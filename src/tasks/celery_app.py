from celery import Celery

from src.settings_config import settings

celery_instance = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)