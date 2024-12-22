from pydantic import BaseModel
from typing import Optional, Any, List

# 定义 AttributeChange，包含属性、数值、操作
class AttributeChange(BaseModel):
    attribute: str
    value: float
    operation: str  # add, subtract, multiply, divide

class OptionBase(BaseModel):
    text: str
    result_attribute_changes: Optional[List[AttributeChange]] = []
    triggers_ending: Optional[bool] = False
    ending_description: Optional[str] = None
    impact_description: Optional[str] = None

class OptionCreate(BaseModel):
    text: str
    result_attribute_changes: Optional[List[AttributeChange]] = []
    triggers_ending: Optional[bool] = False
    ending_description: Optional[str] = None
    impact_description: Optional[str] = None
    event_id: int  # 添加 event_id 字段

class OptionUpdate(BaseModel):
    text: Optional[str] = None
    result_attribute_changes: Optional[List[AttributeChange]] = []
    triggers_ending: Optional[bool] = False
    ending_description: Optional[str] = None
    impact_description: Optional[str] = None

class Option(OptionBase):
    id: int
    event_id: int  # 修改为 int

    class Config:
        orm_mode = True
