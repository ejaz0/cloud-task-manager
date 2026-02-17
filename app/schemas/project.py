from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    title: str

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
