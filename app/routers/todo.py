from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.todo import (
    create_todo,
    get_todo,
    get_todos,
    update_todo,
    delete_todo,
    create_tag,
    get_tags,
    get_tag,
    delete_tag,
)
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoInDB,
    TodoTagCreate,
    TodoTagInDB,
)
from app.database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


# Tag 路由
@router.post("/tags/", response_model=TodoTagInDB)
async def create_tag_endpoint(tag: TodoTagCreate, db: AsyncSession = Depends(get_db)):
    db_tag = await create_tag(db=db, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return db_tag


@router.get("/tags/", response_model=list[TodoTagInDB])
async def read_tags(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    tags = await get_tags(db, skip=skip, limit=limit)
    return tags


@router.get("/tags/{tag_id}", response_model=TodoTagInDB)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    db_tag = await get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete("/tags/{tag_id}", response_model=TodoTagInDB)
async def delete_tag_endpoint(tag_id: int, db: AsyncSession = Depends(get_db)):
    db_tag = await delete_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


# Todo 路由
@router.post("/", response_model=TodoInDB)
async def create_todo_endpoint(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_todo = await create_todo(db=db, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=400, detail="Invalid tag_id")
    return db_todo


@router.get("/{todo_id}", response_model=TodoInDB)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.get("/", response_model=list[TodoInDB])
async def read_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    todos = await get_todos(db, skip=skip, limit=limit)
    return todos


@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo_item(
    todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)
):
    db_todo = await update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found or invalid tag_id")
    return db_todo


@router.delete("/{todo_id}", response_model=TodoInDB)
async def delete_todo_endpoint(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
