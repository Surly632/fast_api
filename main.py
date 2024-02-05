from contextlib import contextmanager
from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from controller.UserController import router as user_route 
import uvicorn

port = 8088

async def lifespan(app:FastAPI):
    print(f'server running on port: {port}')
    yield
    print('server is shutting down...')

def __init__app():
    
    app = FastAPI(
        lifespan=lifespan,
        title='Fast Api with postgresql',
        description='This is a demo',
        # docs_url='/',
        version='1.0.0'
    )
    
    @app.get('/')
    async def homePage():
        data={
            'success':True,
            'message':'Welcome to HomePage'
        }
        return JSONResponse(content=data,status_code=HTTPStatus.OK)
    
    app.include_router(router=user_route)
    from controller.RedisController import router as redis_route
    app.include_router(router=redis_route)
    
    return app

app = __init__app()


if __name__ == '__main__':
    uvicorn.run('main:app',host='localhost',port=8088,reload=True)