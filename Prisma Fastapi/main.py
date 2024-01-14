from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi.responses import JSONResponse
from config import connection
import uvicorn
from fastapi import FastAPI

port = 8088 

@asynccontextmanager
async def lifespan(app:FastAPI):
    print(f'server is running on port: {port} [lifespan]')
    await connection.prima_connection.connect()
    yield
    print(f'server is shutting down...')
    await connection.prima_connection.disconnect()

def init_app():
    app = FastAPI(
        lifespan=lifespan,
        title="prisma connection to database ",
        docs_url="/",
        description="Fast API",
        version="1.0.0"
    )
    
    @app.get('')
    async def homePage():
        data = {
            "success": True,
            "data": "Welcome to the homepage",
        }
        return JSONResponse(content=data,status_code=HTTPStatus.OK);

    
    from controller.PostController import router as route
    app.include_router(router=route) 
    
    return app


app = init_app() 


    

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8088, reload=True)
