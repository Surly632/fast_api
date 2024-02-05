from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(
    url=os.getenv('DATABASE_URL'),
    echo=True
)
session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()
