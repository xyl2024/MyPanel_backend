from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime, timezone


class TodoTag(Base):
    __tablename__ = "todo_tags"
    __table_args__ = {"comment": "待办事项的标签"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系 - 注意 back_populates 的值要与 Todo 模型中的属性名一致
    todos = relationship("Todo", back_populates="tag")
