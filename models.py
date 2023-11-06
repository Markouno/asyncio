import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON



POSTGRES_USER = os.getenv('POSTGRES_USER', 'secret')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'swapi')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'swapi')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

POSTGRES_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs,DeclarativeBase):
    pass


class Character(Base):

    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




