import json
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app.db import models
from app.schemas import task as task_schema
from app.services.cache import cache_service

router = APIRouter()


@router.get("/", response_model=List[task_schema.TaskOut])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    query = db.query(models.Task)
    if project_id:
        # Verify user owns the project or is admin
        project = (
            db.query(models.Project).filter(models.Project.id == project_id).first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if (
            current_user.role != models.UserRole.ADMIN
            and project.owner_id != current_user.id
        ):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        query = query.filter(models.Task.project_id == project_id)
    else:
        if current_user.role != models.UserRole.ADMIN:
            # Users can only see tasks of projects they own
            query = query.join(models.Project).filter(
                models.Project.owner_id == current_user.id
            )

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.post("/", response_model=task_schema.TaskOut)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: task_schema.TaskCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    # Verify project ownership
    project = (
        db.query(models.Project).filter(models.Project.id == task_in.project_id).first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{id}", response_model=task_schema.TaskOut)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    cache_key = f"task:{id}"
    cached_task = cache_service.get(cache_key)
    if cached_task:
        # Permission check for cached data
        if (
            current_user.role != models.UserRole.ADMIN
            and cached_task["owner_id"] != current_user.id
        ):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        return cached_task

    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check ownership via project
    project = (
        db.query(models.Project).filter(models.Project.id == task.project_id).first()
    )
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    task_data = jsonable_encoder(task)
    # Store owner_id in cache for subsequent permission checks
    task_data["owner_id"] = project.owner_id
    cache_service.set(cache_key, task_data)

    return task


@router.put("/{id}", response_model=task_schema.TaskOut)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    task_in: task_schema.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check ownership via project
    project = (
        db.query(models.Project).filter(models.Project.id == task.project_id).first()
    )
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    update_data = task_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(task, field, update_data[field])

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{id}", response_model=task_schema.TaskOut)
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check ownership via project
    project = (
        db.query(models.Project).filter(models.Project.id == task.project_id).first()
    )
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    db.delete(task)
    db.commit()

    # Invalidate cache
    cache_service.delete(f"task:{id}")

    return task
