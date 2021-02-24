from sqlalchemy.ext.asyncio import create_async_engine

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/banksimulator"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)