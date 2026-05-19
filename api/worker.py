#!/usr/bin/env python3
"""
Celery worker startup script for async analytics processing.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.celery_app import celery_app

if __name__ == "__main__":
    # Start Celery worker
    celery_app.start([
        "worker",
        "--loglevel=INFO",
        "--pool=solo",
        "--queues=analytics",
    ])
