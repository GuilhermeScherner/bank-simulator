from app.infraestructure.db.uow import UnitOfWork
import sqlalchemy as sla
import app.application.models.transfer as transfer_models
from aiokafka import AIOKafkaProducer


class TransferService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_users(self):
        qb = sla.select(transfer_models.Users)
        result = await self.uow.execute(qb)
        all_result = result.scalars().all()
        users = list(map(transfer_models.CreateUser.from_orm, all_result))
        return transfer_models.ListUsers(users=users)

    async def create_user(self, user: transfer_models.UserRequest):
        async with self.uow as uow:
            create = transfer_models.Users(**user.dict())
            uow.add(create)
            await uow.commit()
            await uow.refresh(create)
            return transfer_models.UserResponse.from_orm(create)

    async def create_transfer(self, transfer: transfer_models.TransferRequest, producer: AIOKafkaProducer):
        msg_string = "cpf_sender: {cpf_sender}, value: {value}, cpf_receiver: {cpf_receiver}, description: {description}". \
            format(cpf_sender=transfer.cpf_sender, value=transfer.value, cpf_receiver=transfer.cpf_receiver,
                   description=transfer.description)
        msg = bytes(msg_string, encoding='utf-8')

        await producer.send_and_wait(producer.KAFKA_TOPIC, value=msg)
