"""
Celery tasks for async analytics processing.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional
from celery import current_task
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.celery_app import celery_app
from app.db import SessionLocal
from app.models import ClickEvent, Link
from app.redis_client import RedisClient

def generate_idempotency_key(link_id: int, ip_hash: str, user_agent: Optional[str], timestamp_window: int = 300) -> str:
    """
    Generate idempotency key for click events to prevent duplicate counting.
    Uses 5-minute window (300 seconds) by default.
    """
    # Hash user agent for privacy
    ua_hash = hashlib.md5((user_agent or "").encode()).hexdigest()[:8]
    
    # Get timestamp window (floor to nearest 5 minutes)
    now = datetime.now(timezone.utc)
    window_start = int(now.timestamp() // timestamp_window) * timestamp_window
    
    return f"click:{link_id}:{ip_hash}:{ua_hash}:{window_start}"

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def log_click_event(self, link_id: int, ip_hash: str, user_agent: Optional[str] = None, referrer: Optional[str] = None):
    """
    Async task to log click event with idempotency protection.
    """
    task_id = self.request.id
    
    try:
        # Generate idempotency key
        idempotency_key = generate_idempotency_key(link_id, ip_hash, user_agent)
        
        # Check if already processed using Redis
        if RedisClient.get(idempotency_key):
            print(f"Duplicate click detected: {idempotency_key}")
            return {"status": "duplicate", "task_id": task_id}
        
        # Mark as processing
        RedisClient.set(idempotency_key, task_id, ex=3600)  # 1 hour expiry
        
        # Get database session
        db = SessionLocal()
        try:
            # Verify link exists
            link = db.execute(select(Link).where(Link.id == link_id)).scalar_one_or_none()
            if not link:
                raise ValueError(f"Link {link_id} not found")
            
            # Create click event
            click = ClickEvent(
                link_id=link_id,
                ip_hash=ip_hash,
                user_agent=user_agent,
                referrer=referrer
            )
            
            db.add(click)
            db.commit()
            
            print(f"Click event logged: link_id={link_id}, task_id={task_id}")
            return {
                "status": "success", 
                "click_id": click.id,
                "task_id": task_id,
                "idempotency_key": idempotency_key
            }
            
        except Exception as db_error:
            db.rollback()
            # Remove idempotency key on failure so it can be retried
            RedisClient.delete(idempotency_key)
            raise db_error
            
        finally:
            db.close()
            
    except Exception as exc:
        # Retry on transient failures
        if self.request.retries < self.max_retries:
            raise self.retry(exc, countdown=5)
        else:
            print(f"Failed to log click event after {self.max_retries} retries: {exc}")
            return {
                "status": "failed",
                "error": str(exc),
                "task_id": task_id
            }

@celery_app.task
def cleanup_old_click_events(retention_days: int = 90):
    """
    Background task to clean up old click events based on retention policy.
    """
    try:
        db = SessionLocal()
        try:
            cutoff_date = datetime.now(timezone.utc).timestamp() - (retention_days * 24 * 3600)
            
            # Delete old click events
            deleted_count = db.execute(
                "DELETE FROM click_events WHERE created_at < to_timestamp(:cutoff)",
                {"cutoff": cutoff_date}
            ).rowcount
            
            db.commit()
            
            print(f"Cleaned up {deleted_count} old click events (older than {retention_days} days)")
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "retention_days": retention_days
            }
            
        finally:
            db.close()
            
    except Exception as exc:
        print(f"Failed to cleanup old click events: {exc}")
        return {
            "status": "failed",
            "error": str(exc)
        }
