from sqlalchemy.orm import Session
from app.models.endings import Ending
from app.schemas.ending_schemas import EndingCreate, EndingUpdate, Condition

def get_ending(db: Session, ending_id: int):
    return db.query(Ending).filter(Ending.id == ending_id).first()

def get_endings_by_game(db: Session, game_id: int):
    return db.query(Ending).filter(Ending.game_id == game_id).all()

def create_ending(db: Session, ending: EndingCreate):
    db_end = Ending(
        game_id=ending.game_id,
        description=ending.description,
        trigger_conditions=(
            [c.dict() for c in ending.trigger_conditions]
            if ending.trigger_conditions else None
        )
    )
    db.add(db_end)
    db.commit()
    db.refresh(db_end)
    return db_end

def update_ending(db: Session, ending_id: int, ending: EndingUpdate):
    db_end = get_ending(db, ending_id)
    if not db_end:
        return None
    if ending.description is not None:
        db_end.description = ending.description
    if ending.trigger_conditions is not None:
        # 注意 pydantic model 需要转 dict
        db_end.trigger_conditions = [c.dict() for c in ending.trigger_conditions]
    db.commit()
    db.refresh(db_end)
    return db_end

def delete_ending(db: Session, ending_id: int):
    db_end = get_ending(db, ending_id)
    if db_end:
        db.delete(db_end)
        db.commit()
        return True
    return False

def check_ending_conditions(game_state: dict, conditions: list[dict]) -> bool:
    """
    game_state: 
      {
        "attributes": {"strength": 12, "intelligence": 3, ...},
        "items": {"神秘钥匙": 1, "绷带": 2},  # 或者用list也行
        "flags": {"is_vip_user": True, "joined_dark_guild": False}
      }
    conditions: 
      [
        {"type": "attribute", "attribute": "strength", "operator": ">=", "value": 10},
        {"type": "flag", "flag_name": "is_vip_user", "required_value": true},
        {"type": "item", "item_name": "神秘钥匙"}
      ]
    """
    if not conditions:
        # 如果没有设置任何条件，默认就算通过
        return True
    
    for cond in conditions:
        cond_type = cond.get("type", "attribute")
        
        if cond_type == "attribute":
            attr_name = cond.get("attribute")
            op = cond.get("operator")
            target_value = cond.get("value", 0)
            current_value = game_state["attributes"].get(attr_name, 0)
            
            if not evaluate_attribute_condition(current_value, op, target_value):
                return False
        
        elif cond_type == "item":
            item_name = cond.get("item_name")
            # 看看是否拥有这个物品
            # 如果你用 list 来存储 items，就需要: `if item_name not in game_state["items"]`
            # 如果你用 dict 存储 items 及数量：
            if item_name not in game_state["items"]:
                return False
        
        elif cond_type == "flag":
            flag_name = cond.get("flag_name")
            required_value = cond.get("required_value", True)
            actual_value = game_state["flags"].get(flag_name, False)
            if actual_value != required_value:
                return False
        
        else:
            # 其它类型自己扩展
            pass
    
    return True

def evaluate_attribute_condition(current_value: float, operator: str, target_value: float) -> bool:
    if operator == ">":
        return current_value > target_value
    elif operator == ">=":
        return current_value >= target_value
    elif operator == "<":
        return current_value < target_value
    elif operator == "<=":
        return current_value <= target_value
    elif operator == "==":
        return current_value == target_value
    else:
        # 未知 operator，就当不通过
        return False
