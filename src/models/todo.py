from sqlalchemy import (
    func,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime, timezone


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {"comment": "待办事项"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True, comment="支持Markdown格式的描述")
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True, comment="预期完成时间")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tag_id = Column(Integer, ForeignKey("todo_tags.id"), nullable=False)
    tag = relationship("TodoTag", back_populates="todos")
