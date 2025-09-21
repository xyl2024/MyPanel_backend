from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models.todo import Todo
from app.models.todo_tag import TodoTag
from app.schemas.todo import TodoCreate, TodoUpdate, TodoTagCreate

# Tag CRUD 操作
async def get_tag(db: AsyncSession, tag_id: int):
    result = await db.execute(select(TodoTag).where(TodoTag.id == tag_id))
    return result.scalar_one_or_none()

async def get_tag_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(TodoTag).where(TodoTag.name == name))
    return result.scalar_one_or_none()

async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(TodoTag).offset(skip).limit(limit))
    return result.scalars().all()

async def create_tag(db: AsyncSession, tag: TodoTagCreate):
    db_tag = TodoTag(**tag.model_dump())
    db.add(db_tag)
    try:
        await db.commit()
        await db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        await db.rollback()
        return None

async def delete_tag(db: AsyncSession, tag_id: int):
    db_tag = await get_tag(db, tag_id)
    if db_tag:
        await db.delete(db_tag)
        await db.commit()
    return db_tag

# Todo CRUD 操作
async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(
        select(Todo)
        .where(Todo.id == todo_id)
        .options(selectinload(Todo.tag))
    )
    return result.scalar_one_or_none()

async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Todo)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Todo.tag))
    )
    return result.scalars().all()

async def create_todo(db: AsyncSession, todo: TodoCreate):
    # 检查 tag 是否存在
    tag = await get_tag(db, todo.tag_id)
    if not tag:
        return None
    
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    
    # 重新加载关联的 tag
    await db.refresh(db_todo, ["tag"])
    return db_todo

async def update_todo(db: AsyncSession, todo_id: int, todo: TodoUpdate):
    db_todo = await get_todo(db, todo_id)
    if db_todo:
        update_data = todo.model_dump(exclude_unset=True)
        
        # 如果要更新 tag_id，先检查 tag 是否存在
        if "tag_id" in update_data:
            tag = await get_tag(db, update_data["tag_id"])
            if not tag:
                return None
        
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        await db.commit()
        await db.refresh(db_todo)
        await db.refresh(db_todo, ["tag"])
    return db_todo

async def delete_todo(db: AsyncSession, todo_id: int):
    db_todo = await get_todo(db, todo_id)
    if db_todo:
        await db.delete(db_todo)
        await db.commit()
    return db_todo