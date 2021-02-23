from app.infraestructure.db.uow import UnitOfWork
import sqlalchemy as sla
import app.application.models.transfer as transfer_models
from app.infraestructure.mappings.transfer import Users
from aiokafka import AIOKafkaProducer
from app.setting.producer.producer import KAFKA_TOPIC



class TransferService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_users(self):
        qb = sla.select(Users)
        result = await self.uow.session.execute(qb)
        all_result = result.scalars().all()
        users = list(map(transfer_models.CreateUser.from_orm, all_result))
        return transfer_models.ListUsers(users=users)

    async def create_user(self, user: transfer_models.UserRequest):
        async with self.uow as uow:
            create = Users(**user.dict())
            uow.session.add(create)
            await uow.session.commit()
            await uow.session.refresh(create)
            return transfer_models.UserResponse.from_orm(create)

    async def create_transfer(self, transfer: transfer_models.TransferRequest, producer: AIOKafkaProducer):
        msg_string = "cpf_sender: {cpf_sender}, value: {value}, cpf_receiver: {cpf_receiver}, description: {description}". \
            format(cpf_sender=transfer.cpf_sender, value=transfer.value, cpf_receiver=transfer.cpf_receiver,
                   description=transfer.description)
        msg = bytes(msg_string, encoding='utf-8')
        await producer.send_and_wait(KAFKA_TOPIC, value=msg)
