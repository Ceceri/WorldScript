from sqlalchemy.orm import Session
from app.models.events import GameEvent
from app.schemas.event_schemas import EventCreate, EventUpdate
from fastapi import HTTPException
from app.models.options import GameOption  # 导入 GameOption 模型
from app.crud.option_crud import create_option
from app.schemas.option_schemas import OptionCreate

def get_event(db: Session, event_id: str):
    return db.query(GameEvent).filter(GameEvent.id == event_id).first()

def get_events_by_game(db: Session, game_id: int, skip: int = 0, limit: int = 100):
    return db.query(GameEvent).filter(GameEvent.game_id == game_id).offset(skip).limit(limit).all()

def create_event(db: Session, event: EventCreate):
    # 检查数据库中是否已存在相同 ID 的事件
    existing_event = db.query(GameEvent).filter(GameEvent.id == event.id).first()
    if existing_event:
        raise HTTPException(status_code=400, detail="事件 ID 已存在，请使用不同的 ID。")

    # 将 range_condition 转换为字典（如果存在）
    range_condition_dict = event.range_condition.dict() if event.range_condition else None

    # 插入新事件
    db_event = GameEvent(
        id=event.id,
        game_id=event.game_id,
        title=event.title,
        description=event.description,
        range_condition=range_condition_dict
    )
    db.add(db_event)
    db.commit()  # 提交事件保存
    db.refresh(db_event)

    # 保存选项
    if hasattr(event, 'options') and event.options:
        for option_data in event.options:
            option_data.event_id = db_event.id  # 关联事件 ID
            create_option(db, OptionCreate(**option_data.dict()))  # 调用选项保存逻辑

    db.commit()  # 提交选项保存
    db.refresh(db_event)
    return db_event




def update_event(db: Session, event_id: str, event: EventUpdate):
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    if event.title is not None:
        db_event.title = event.title
    if event.description is not None:
        db_event.description = event.description
    if event.range_condition is not None:
        db_event.range_condition = event.range_condition
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: str):
    # 先删除关联的选项记录
    db.query(GameOption).filter(GameOption.event_id == event_id).delete()

    # 删除事件记录
    db_event = get_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False