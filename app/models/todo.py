from sqlalchemy import func, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {"comment": "待办事项"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    tag_id = Column(Integer, ForeignKey("todo_tags.id"), nullable=False)
    tag = relationship("TodoTag", back_populates="todos")
