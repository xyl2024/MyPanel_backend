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


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {"comment": "待办事项"}

    id = Column(Integer, primary_key=True, index=True, comment="待办事项唯一标识")
    title = Column(String, index=True, comment="待办事项标题")
    description = Column(Text, nullable=True, comment="支持Markdown格式的描述")
    completed = Column(Boolean, default=False, comment="是否已完成")
    due_date = Column(DateTime, nullable=True, comment="预期完成时间")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    tag_id = Column(Integer, ForeignKey("todo_tags.id"), nullable=False, comment="待办事项标签ID")
    # 关系 - 注意 back_populates 的值要与 TodoTag 模型中的属性名一致
    tag = relationship("TodoTag", back_populates="todos")
