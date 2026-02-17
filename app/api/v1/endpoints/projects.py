from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db import models
from app.schemas import project as project_schema

router = APIRouter()


@router.get("/", response_model=List[project_schema.ProjectOut])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    if current_user.role == models.UserRole.ADMIN:
        projects = db.query(models.Project).offset(skip).limit(limit).all()
    else:
        projects = (
            db.query(models.Project)
            .filter(models.Project.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return projects


@router.post("/", response_model=project_schema.ProjectOut)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: project_schema.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = models.Project(**project_in.dict(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{id}", response_model=project_schema.ProjectOut)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return project


@router.put("/{id}", response_model=project_schema.ProjectOut)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    project_in: project_schema.ProjectUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    update_data = project_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(project, field, update_data[field])

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{id}", response_model=project_schema.ProjectOut)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if (
        current_user.role != models.UserRole.ADMIN
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    db.delete(project)
    db.commit()
    return project
