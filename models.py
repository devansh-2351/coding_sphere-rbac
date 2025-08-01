from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import validator

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    role: str = Field(default="user")
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'admin']:
            raise ValueError('Role must be either "user" or "admin"')
        return v

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserLogin(SQLModel):
    username: str
    password: str

class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
