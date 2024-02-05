from config.database import session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db()->AsyncSession:
        try:
            async with session() as db:
                await db.begin()
                yield db
        finally:
            await db.close()
