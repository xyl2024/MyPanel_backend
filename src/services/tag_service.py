from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models.todo_tag import TodoTag
from src.repositories.tag_repository import TagRepository
from src.schemas.todo import TodoTagCreate

class TagService:
    def __init__(self, tag_repo: TagRepository):
        self.tag_repo = tag_repo
    
    async def get_tag(self, tag_id: int) -> TodoTag:
        tag = await self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag
    
    async def get_tags(self, skip: int = 0, limit: int = 100) -> List[TodoTag]:
        return await self.tag_repo.get_all(skip, limit)
    
    async def create_tag(self, tag_create: TodoTagCreate) -> TodoTag:
        # 检查标签名是否已存在
        existing_tag = await self.tag_repo.get_by_name(tag_create.name)
        if existing_tag:
            raise HTTPException(status_code=400, detail="Tag already exists")
        
        return await self.tag_repo.create(**tag_create.model_dump())
    
    async def delete_tag(self, tag_id: int) -> TodoTag:
        tag = await self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        
        await self.tag_repo.delete(tag)
        return tag