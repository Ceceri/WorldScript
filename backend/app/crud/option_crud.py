from sqlalchemy.orm import Session
from app.models.options import GameOption
from app.schemas.option_schemas import OptionCreate, OptionUpdate
from app.schemas.option_schemas import AttributeChange

def get_option(db: Session, option_id: int):
    db_option = db.query(GameOption).filter(GameOption.id == option_id).first()
    if db_option and db_option.result_attribute_changes:
        db_option.result_attribute_changes = AttributeChange(**db_option.result_attribute_changes)
    return db_option

def get_options_by_event(db: Session, event_id: int):
    db_options = db.query(GameOption).filter(GameOption.event_id == event_id).all()
    for option in db_options:
        if option.result_attribute_changes:
            # 确保逐个解析列表中的每个变化
            option.result_attribute_changes = [
                AttributeChange(**change) for change in option.result_attribute_changes
            ]
    return db_options


def create_option(db: Session, option: OptionCreate):
    # 检查是否已存在相同的选项
    existing_option = db.query(GameOption).filter(
        GameOption.event_id == option.event_id,
        GameOption.text == option.text
    ).first()

    if existing_option:
        print(f"Option already exists: event_id={option.event_id}, text={option.text}")
        return existing_option  # 如果已存在，直接返回

    # 如果不存在，创建新的选项
    db_option = GameOption(
        event_id=option.event_id,
        text=option.text,
        result_attribute_changes=[
            change.dict() for change in option.result_attribute_changes
        ] if option.result_attribute_changes else None,
        triggers_ending=option.triggers_ending,
        ending_description=option.ending_description,
        impact_description=option.impact_description
    )
    db.add(db_option)
    return db_option  # 不提交事务，由调用方统一提交




def update_option(db: Session, option_id: int, option: OptionUpdate):
    db_option = get_option(db, option_id)
    if not db_option:
        return None
    if option.text is not None:
        db_option.text = option.text
    if option.result_attribute_changes is not None:
        db_option.result_attribute_changes = option.result_attribute_changes.dict()
    if option.triggers_ending is not None:
        db_option.triggers_ending = option.triggers_ending
    if option.ending_description is not None:
        db_option.ending_description = option.ending_description
    if option.impact_description is not None: 
        db_option.impact_description = option.impact_description
    db.commit()
    db.refresh(db_option)
    return db_option


def delete_option(db: Session, option_id: int):
    db_option = get_option(db, option_id)
    if db_option:
        db.delete(db_option)
        db.commit()
        return True
    return False

