from model.pydantic.UserModel import UserModel as db_user
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repository.UserRepository import UserRepository

user_repo = UserRepository()

class UserService:
    @staticmethod
    async def create_user(user_data:db_user,db:AsyncSession):
        return  await user_repo.create_user(user_data,db)
    
    