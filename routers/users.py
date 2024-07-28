from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database_interaction import get_db
from handlers import _create_new_user
from models import UserCreate, ShowUser

user_router = APIRouter()


@user_router.post('/', response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, session)
