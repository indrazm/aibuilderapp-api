from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SQLEnum
from sqlmodel import JSON, Field, Relationship

from app.core.models import BaseModel


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Project(BaseModel, table=True):
    name: str = Field(default="App Project")
    description: Optional[str] = None
    port: int = Field(unique=True)
    server_pid: Optional[int] = Field(default=None)
    status: ProjectStatus = Field(
        default=ProjectStatus.ACTIVE, sa_type=SQLEnum("active", "inactive", name="projectstatus")
    )

    project_metadata: Optional[dict] = Field(default_factory=dict, sa_type=JSON)
    sessions: List["Session"] = Relationship(back_populates="project", cascade_delete=True)


class Session(BaseModel, table=True):
    project_id: str = Field(foreign_key="project.id")
    name: str = Field(default="App Session")
    messages: Optional[List[dict]] = Field(default=None, sa_type=JSON)

    project: Project = Relationship(back_populates="sessions")
