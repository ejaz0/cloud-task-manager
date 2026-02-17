from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.db.models import TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO


class TaskCreate(TaskBase):
    title: str
    project_id: int


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True
