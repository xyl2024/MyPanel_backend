from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoTagBase(BaseModel):
    name: str


class TodoTagCreate(TodoTagBase):
    pass


class TodoTagInDB(TodoTagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    due_date: Optional[datetime] = None
    tag_id: int


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    tag_name: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    tag_name: Optional[str] = None


class TodoInDB(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tag: TodoTagInDB

    class Config:
        from_attributes = True
