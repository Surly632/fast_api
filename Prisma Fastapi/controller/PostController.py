from fastapi import APIRouter
from service.post_service import PostService
from model import model

router = APIRouter(prefix='/post')

@router.get("/")
async def get_all():
    res = await PostService.get_all()
    return res
   

# @router.post('/create')
# async def create_post(request:model.Post):
#     res = await PostService.create_post(request)
#     return res; 