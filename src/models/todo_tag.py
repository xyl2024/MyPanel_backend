from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class TodoTag(Base):
    __tablename__ = "todo_tags"
    __table_args__ = {"comment": "待办事项标签"}

    id = Column(Integer, primary_key=True, index=True, comment="待办标签唯一标识")
    name = Column(String, unique=True, index=True, nullable=False, comment="待办标签名")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系 - 注意 back_populates 的值要与 Todo 模型中的属性名一致
    todos = relationship("Todo", back_populates="tag")
