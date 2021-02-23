from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr
from typing import Any
import re

Base = declarative_base()


def camel_to_snake(name: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
