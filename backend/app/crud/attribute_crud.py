from sqlalchemy.orm import Session
from app.models.attributes import PlayerAttribute
from app.schemas.attribute_schemas import AttributeCreate, AttributeUpdate

def get_attribute(db: Session, attribute_id: int):
    return db.query(PlayerAttribute).filter(PlayerAttribute.id == attribute_id).first()

def get_attributes_by_game(db: Session, game_id: int):
    return db.query(PlayerAttribute).filter(PlayerAttribute.game_id == game_id).all()

def create_attribute(db: Session, attribute: AttributeCreate):
    db_attr = PlayerAttribute(
        game_id=attribute.game_id,
        name=attribute.name,
        initial_value=attribute.initial_value
    )
    db.add(db_attr)
    db.commit()
    db.refresh(db_attr)
    return db_attr

def update_attribute(db: Session, attribute_id: int, attribute: AttributeUpdate):
    db_attr = db.query(PlayerAttribute).filter(PlayerAttribute.id == attribute_id).first()
    if not db_attr:
        print(f"Attribute with ID {attribute_id} not found.")
        return None

    # 输出接收到的更新数据
    update_data = attribute.dict(exclude_unset=True)  # exclude_unset: 排除未传入的字段
    print(f"Update data: {update_data}")

    for key, value in update_data.items():
        print(f"Updating {key} to {value}")
        setattr(db_attr, key, value)

    db.commit()
    db.refresh(db_attr)
    print("Attribute successfully updated.")
    return db_attr



def delete_attribute(db: Session, attribute_id: int):
    db_attr = get_attribute(db, attribute_id)
    if db_attr:
        db.delete(db_attr)
        db.commit()
        return True
    return False

