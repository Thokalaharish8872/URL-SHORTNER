"""
Celery app configuration for async analytics processing.
"""

from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "analytics_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30,  # 30 seconds per task
    task_soft_time_limit=25,  # 25 seconds soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Retry configuration
celery_app.conf.update(
    task_acks_late=True,
    worker_disable_rate_limits=False,
    task_reject_on_worker_lost=True,
)

# Queue configuration
celery_app.conf.update(
    task_routes={
        "app.tasks.log_click_event": {"queue": "analytics"},
    }
)
