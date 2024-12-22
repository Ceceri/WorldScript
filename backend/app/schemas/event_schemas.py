from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from app.schemas.option_schemas import OptionCreate

class EventBase(BaseModel):
    title: str
    description: Optional[str]
    range_condition: Optional[Any]

class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    range_condition: Optional[Any]


class EventResponse(BaseModel):
    id: int
    game_id: int
    title: str
    description: Optional[str] = None
    range_condition: Optional[Dict] = None

    class Config:
        from_attributes = True  # 使用 ORM 模型时需要此选项

class Event(EventBase):
    id: int
    game_id: int

    class Config:
        orm_mode = True

class RangeCondition(BaseModel):
    attribute: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None

class EventCreate(BaseModel):
    id: int
    game_id: int
    title: str
    description: Optional[str] = None
    range_condition: Optional[RangeCondition] = None
    options: List[OptionCreate] = []  # 添加选项字段


class EventOption(BaseModel):
    text: str
    result_attribute_changes: Dict[str, Dict[str, str]]
    impact_description: str

class EventLLMGenerateRequest(BaseModel):
    title: str
    description: str
    background: str  # 背景字段

class EventLLMGenerateResponse(BaseModel):
    extended_description: str
    options: List[EventOption]