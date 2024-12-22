from pydantic import BaseModel, Field
from typing import Optional

class AttributeBase(BaseModel):
    name: str
    initial_value: float

class AttributeCreate(AttributeBase):
    game_id: int


class AttributeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the attribute")
    initial_value: Optional[float] = Field(None, description="Initial value of the attribute")

    class Config:
        extra = 'ignore'  # 忽略未定义的字段（确保不会报错）


class Attribute(AttributeBase):
    id: int
    game_id: int

    class Config:
        orm_mode = True
