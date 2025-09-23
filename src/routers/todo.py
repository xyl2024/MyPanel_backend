from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.repositories.todo_repository import TodoRepository
from src.repositories.tag_repository import TagRepository
from src.services.todo_service import TodoService
from src.services.tag_service import TagService
from src.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoInDB,
    TodoTagCreate,
    TodoTagInDB,
)

router = APIRouter(prefix="/todos", tags=["todos"])


# 依赖注入函数
async def get_todo_service(db: AsyncSession = Depends(get_db)):
    todo_repo = TodoRepository(db)
    tag_repo = TagRepository(db)
    return TodoService(todo_repo, tag_repo)


async def get_tag_service(db: AsyncSession = Depends(get_db)):
    tag_repo = TagRepository(db)
    return TagService(tag_repo)


# Tag 路由
@router.post("/tags/", response_model=TodoTagInDB)
async def create_tag(
    tag: TodoTagCreate, service: TagService = Depends(get_tag_service)
):
    """
    创建待办事项标签
    """
    return await service.create_tag(tag)


@router.get("/tags/", response_model=list[TodoTagInDB])
async def get_tags(
    skip: int = 0, limit: int = 100, service: TagService = Depends(get_tag_service)
):
    return await service.get_tags(skip=skip, limit=limit)


@router.get("/tags/{tag_id}", response_model=TodoTagInDB)
async def get_tag(tag_id: int, service: TagService = Depends(get_tag_service)):
    return await service.get_tag(tag_id)


@router.delete("/tags/{tag_id}", response_model=TodoTagInDB)
async def delete_tag(
    tag_id: int, service: TagService = Depends(get_tag_service)
):
    return await service.delete_tag(tag_id)


# Todo 路由
@router.post("/", response_model=TodoInDB)
async def create_todo(
    todo: TodoCreate,  # 使用新的 TodoCreate 模型
    service: TodoService = Depends(get_todo_service),
):
    """
    创建待办事项
    """
    return await service.create_todo(todo)


@router.get("/{todo_id}", response_model=TodoInDB)
async def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    return await service.get_todo(todo_id)


@router.get("/", response_model=list[TodoInDB])
async def get_todos(
    skip: int = 0, limit: int = 100, service: TodoService = Depends(get_todo_service)
):
    return await service.get_todos(skip=skip, limit=limit)


@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo_item(
    todo_id: int,
    todo: TodoUpdate,  # 使用新的 TodoUpdate 模型
    service: TodoService = Depends(get_todo_service),
):
    return await service.update_todo(todo_id, todo)


@router.delete("/{todo_id}", response_model=TodoInDB)
async def delete_todo(
    todo_id: int, service: TodoService = Depends(get_todo_service)
):
    return await service.delete_todo(todo_id)
