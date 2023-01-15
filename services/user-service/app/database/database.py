from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator
from fastapi import FastAPI, Depends

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String(length=128), nullable=False)
    last_name = Column(String(length=128), nullable=False)

class DatabaseInitializer():
    def __init__(self) -> None:
        self.engine = None
        self.async_session_maker = None

    def init_database(self, postgres_dsn):
        self.engine = create_async_engine(postgres_dsn)
        self.async_session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


DB_INITIALIZER = DatabaseInitializer()

async def create_db_and_tables():
    async with DB_INITIALIZER.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with DB_INITIALIZER.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)