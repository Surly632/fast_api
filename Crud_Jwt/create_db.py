from config.database import engine,Base
import asyncio

async def create_db():
    async with engine.begin() as conn:
        from model.database import NoteModel
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    
asyncio.run(create_db())
