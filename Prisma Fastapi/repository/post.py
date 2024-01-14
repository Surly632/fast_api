import uuid
from config.connection import prima_connection
from model.model import Post

class PostRepository:
    @staticmethod
    async def get_all():
        return await prima_connection.prisma.post_table.query_raw(
            '''
            select * from post
            '''
        )
    
    @staticmethod
    async def create_post(request:Post):
        return await prima_connection.prisma.post.create({
            'title':request.title,
            'description':request.description,
        })
    @staticmethod
    async def find_by_id(id: uuid.UUID):
        return await prima_connection.prisma.post.find_first(
            where={"id":Post.id}
        )
    @staticmethod 
    async def delete_post(post_id:uuid.UUID):
        return await prima_connection.prisma.post.delete(
            where={
                'id':post_id
            }
        )
    
    