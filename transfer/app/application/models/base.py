import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True
