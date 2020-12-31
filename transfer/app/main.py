from fastapi import FastAPI, HTTPException
import pydantic
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, func


app = FastAPI()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/banksimulator"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

Base = declarative_base()


class Transfer(Base):
    __tablename__ = "transfer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Float)
    cpf = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class TranferRequest(BaseModel):
    name: str
    value: float
    cpf: str


class TransferResponse(BaseModel):
    id: int


@app.post("/transfer", response_model=TransferResponse)
async def create_transfer(transfer: TranferRequest) -> TransferResponse:
    try:
        return {id: 10}
    except:
        raise HTTPException(status_code=404, detail="ERROR")