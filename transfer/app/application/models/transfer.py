from app.application.models.base import BaseModel
from typing import List


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
