from __future__ import annotations

from fastapi import FastAPI, HTTPException, Depends
import pydantic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import sqlalchemy as sla
from typing import List
from aiokafka import AIOKafkaProducer
import os
import asyncio
from dotenv import load_dotenv
from typing import Callable, Type
from functools import cached_property

app = FastAPI()

load_dotenv()
KAFKA_TOPIC1 = os.getenv('KAFKA_TOPIC')
loop = asyncio.get_event_loop()

producer = AIOKafkaProducer(
    loop=loop, client_id="money-transfer", bootstrap_servers="localhost:9092"
)


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/banksimulator"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

Base = declarative_base()


class BaseService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_transfer(self, transfer: TransferRequest):
        
        with self.uow as uow:
            uow.transfer.xambaolage(transfer)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    balance = Column(Float)


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name: str
    cpf: str
    balance: float


class ListUsers(BaseModel):
    users: List[CreateUser]


class TransferRequest(BaseModel):
    cpf_sender: str
    value: float
    cpf_receiver: str
    description: str


class UserRequest(BaseModel):
    name: str
    cpf: str
    balance: float


class TransferResponse(BaseModel):
    id: int


class UserResponse(BaseModel):
    id: int


async def get_db() -> None:
    db = AsyncSession(engine)
    try:
        yield db
    finally:
        await db.close()


@app.on_event("startup")
async def startup_event() -> None:
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await producer.stop()


@app.get("/users", response_model=ListUsers)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> ListUsers:

    qb = sla.select(Users)
    result = await db.execute(qb)
    all_result = result.scalars().all()
    users = list(map(CreateUser.from_orm, all_result))
    return ListUsers(users=users)


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserRequest, db: AsyncSession = Depends(get_db)) -> UserResponse:
    create = Users(**user.dict())
    db.add(create)
    await db.commit()
    await db.refresh(create)
    return UserResponse.from_orm(create)


def service(service_type: Type[BaseService]) -> Callable[[AsyncSession], BaseService]:
    def _get_service(async_session: AsyncSession = Depends(get_db)) -> BaseService:
        return service_type(UnitOfWork(async_session))

    return _get_service



@app.post("/transfer")
async def create_transfer(transfer: TransferRequest,
                          service_transfer: BaseService = Depends(service(BaseService))):

    try:
        service_transfer.create_transfer(transfer)
        msg_string = "cpf_sender: {cpf_sender}, value: {value}, cpf_receiver: {cpf_receiver}, description: {description}".\
            format(cpf_sender=transfer.cpf_sender, value=transfer.value, cpf_receiver=transfer.cpf_receiver,
                   description=transfer.description)
        msg = bytes(msg_string, encoding='utf-8')

        await producer.send_and_wait(KAFKA_TOPIC1, value=msg)
        return {"Result": "Success"}
    except:
        raise HTTPException(status_code=404, detail="Transition has not success")


class UnitOfWork:
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback) -> None:
        if exec_type:
            self.rollback()
        else:
            self.commit()

    def rollback(self) -> None:
        self.async_session.rollback()

    def commit(self) -> None:
        self.async_session.commit()

    @cached_property
    def transfer(self) -> TransferRepository:
        return TransferRepository(self.session)


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def xambaolage(self, transfer: TransferRequest):
        qb = sla.select(Users).where(Users.cpf == transfer.cpf_receiver)
        exe = await self.db.execute(qb)
        balance_receiver = (exe.scalars().first()).balance

        qb = sla.select(Users).where(Users.cpf == transfer.cpf_sender)
        exe = await self.db.execute(qb)
        balance_sender = (exe.scalars().first()).balance

        qb = sla.update(Users).where(Users.cpf == transfer.cpf_receiver).values(
            balance=balance_receiver + transfer.value)

        await self.db.execute(qb)

        qb = sla.update(Users).where(Users.cpf == transfer.cpf_sender).values(balance=balance_sender - transfer.value)

        await self.db.execute(qb)

        await self.db.commit()


class TransferRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)




