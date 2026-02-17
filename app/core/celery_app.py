from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=str(settings.CELERY_BROKER_URL),
    backend=str(settings.CELERY_RESULT_BACKEND),
)

celery_app.conf.task_routes = {
    "app.tasks.sample_tasks.*": "main-queue",
}

celery_app.autodiscover_tasks(["app.tasks"])
