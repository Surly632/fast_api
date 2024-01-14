import uuid
# from model.model import Post
from repository.post import PostRepository


class PostService:
    @staticmethod
    async def get_all():
        return await PostRepository.get_all();
    # @staticmethod 
    # async def create_post(data:Post):
    #     return await PostRepository.create_post(data)
    
    # @staticmethod
    # async def delete_post(data:uuid.UUID):
    #     return await PostRepository.delete_post(data)
    