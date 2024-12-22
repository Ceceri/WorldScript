from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class Condition(BaseModel):
    """
    用于描述单个触发条件：
    - type: "attribute" / "item" / "flag" / 其它
    - attribute / operator / value: 专门给属性数值比较用
    - item_name: 专门给物品判断用
    - flag_name / required_value: 专门给flag判断用
    """
    type: str  # "attribute", "item", "flag", ...
    
    # 如果是属性类型
    attribute: Optional[str] = None
    operator: Optional[str] = None  # ">", ">=", "<", "<=", "=="
    value: Optional[float] = None   # 用于数值比较
    
    # 如果是物品类型
    item_name: Optional[str] = None
    
    # 如果是flag类型
    flag_name: Optional[str] = None
    required_value: Optional[bool] = True

class EndingBase(BaseModel):
    description: Optional[str]
    # 改为列表里放多个 Condition
    trigger_conditions: Optional[List[Condition]] = None

class EndingCreate(EndingBase):
    game_id: int

class EndingUpdate(EndingBase):
    pass

class Ending(EndingBase):
    id: int
    game_id: int

    class Config:
        orm_mode = True
