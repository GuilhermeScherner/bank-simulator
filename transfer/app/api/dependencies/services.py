from app.infraestructure.db.uow import UnitOfWork
from fastapi import Depends
from app.api.dependencies.get_uow import get_uow
from app.application.services.transfer import TransferService


def transfer_service(uow: UnitOfWork = Depends(get_uow)) -> TransferService:
    return TransferService(uow)