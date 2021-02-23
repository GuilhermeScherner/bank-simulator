from sqlalchemy import Column, Integer, Float, String
from app.infraestructure.mappings.base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    balance = Column(Float)