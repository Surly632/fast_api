from model.pydantic.UserModel import UserModel as db_user
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @staticmethod
    async def create_user(user_data: db_user,db:AsyncSession):
        db.add(user_data)
        await db.commit()
        payload = {
            'success':True,
            'data' : user_data
        }
        return payload