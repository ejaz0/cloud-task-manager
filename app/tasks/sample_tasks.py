import time

import structlog

from app.core.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task(name="sample_task")
def sample_task(name: str):
    logger.info(f"Starting sample task for {name}")
    time.sleep(5)
    logger.info(f"Finished sample task for {name}")
    return f"Hello {name}, task completed!"
