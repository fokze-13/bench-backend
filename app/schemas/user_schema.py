from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserRead(BaseModel):
    id: int
    name: str
    balance: float

    model_config = {"from_attributes": True}
