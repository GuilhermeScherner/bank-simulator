from fastapi import APIRouter, Depends, HTTPException
from app.setting.producer.producer import producer
from app.application.services.transfer import TransferService
import app.application.models.transfer as transfer_models
from app.api.dependencies.services import transfer_service

route = APIRouter()


@route.on_event("startup")
async def startup_event() -> None:
    await producer.start()


@route.on_event("shutdown")
async def shutdown_event() -> None:
    await producer.stop()


@route.get("/users", response_model=transfer_models.ListUsers)
async def get_all_users(services: TransferService = Depends(transfer_service)) -> transfer_models.ListUsers:
    try:
        users = await services.get_all_users()
        return users
    except:
        raise HTTPException(status_code=404, detail="Find users has not success")


@route.post("/users", response_model=transfer_models.UserResponse)
async def create_user(user: transfer_models.UserRequest,
                      services: TransferService = Depends(transfer_service)) -> transfer_models.UserResponse:
    try:
        user = await services.create_user(user)
        return user
    except:
        raise HTTPException(status_code=404, detail="Create user has not success")


@route.post("/transfer.py")
async def create_transfer(transfer: transfer_models.TransferRequest,
                          services: TransferService = Depends(transfer_service)):
    try:
        await services.create_transfer(transfer)
        return {"Result": "Success"}
    except:
        raise HTTPException(status_code=404, detail="Transition has not success")
