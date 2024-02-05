from dataclasses import dataclass

import aioredis
from config.redis_config import get_redis
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix='/redis')

@dataclass
class user:
    name:str
    username:str
    value:str

@router.post('/create')
async def createRedisUser(req:Request,redis:aioredis=Depends(get_redis)):
    user_data = req.json()
    return user_data 