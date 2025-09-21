# src/services/todo_service.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models.todo import Todo
from src.models.todo_tag import TodoTag
from src.repositories.todo_repository import TodoRepository
from src.repositories.tag_repository import TagRepository
from src.schemas.todo import TodoCreate, TodoUpdate

class TodoService:
    def __init__(self, todo_repo: TodoRepository, tag_repo: TagRepository):
        self.todo_repo = todo_repo
        self.tag_repo = tag_repo
    
    async def get_todo(self, todo_id: int) -> Todo:
        todo = await self.todo_repo.get_by_id_with_tag(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    
    async def get_todos(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        return await self.todo_repo.get_all_with_tags(skip, limit)
    
    async def create_todo(self, todo_create: TodoCreate) -> Todo:
        # 根据标签名查找或创建标签
        tag = await self.tag_repo.get_by_name(todo_create.tag_name)
        if not tag:
            # 自动创建标签
            tag = await self.tag_repo.create(name=todo_create.tag_name)
        
        # 准备创建待办事项的数据
        todo_data = {
            "title": todo_create.title,
            "description": todo_create.description,
            "due_date": todo_create.due_date,
            "tag_id": tag.id
        }
        
        # 创建待办事项
        todo = await self.todo_repo.create(**todo_data)
        
        # 重要：重新加载带tag的关系，确保序列化时不会出错
        return await self.todo_repo.get_by_id_with_tag(todo.id)
    
    async def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Todo:
        # 获取现有待办事项
        todo = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # 准备更新数据
        update_data = todo_update.model_dump(exclude_unset=True)
        
        # 如果要更新标签名，查找或创建标签
        if "tag_name" in update_data:
            tag = await self.tag_repo.get_by_name(update_data["tag_name"])
            if not tag:
                tag = await self.tag_repo.create(name=update_data["tag_name"])
            update_data["tag_id"] = tag.id
            del update_data["tag_name"]  # 移除 tag_name，因为我们使用 tag_id
        
        # 更新待办事项
        updated_todo = await self.todo_repo.update(todo, **update_data)
        
        # 重新加载关联的标签
        return await self.todo_repo.get_by_id_with_tag(todo_id)
    
    async def delete_todo(self, todo_id: int) -> Todo:
        todo = await self.todo_repo.get_by_id_with_tag(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        await self.todo_repo.delete(todo)
        return todo