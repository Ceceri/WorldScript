from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.attribute_schemas import Attribute, AttributeCreate, AttributeUpdate
from app.crud import attribute_crud
from typing import List
from app.models.attributes import PlayerAttribute  # 导入 PlayerAttribute 模型

router = APIRouter(prefix="/attributes", tags=["attributes"])

@router.post("/", response_model=Attribute)
def create_new_attribute(attribute: AttributeCreate, db: Session = Depends(get_db)):
    return attribute_crud.create_attribute(db, attribute)

@router.get("/{attribute_id}", response_model=Attribute)
def read_attribute(attribute_id: int, db: Session = Depends(get_db)):
    db_attr = attribute_crud.get_attribute(db, attribute_id)
    if not db_attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return db_attr

@router.get("/", response_model=List[Attribute])
def read_attributes_by_game(game_id: int = Query(...), db: Session = Depends(get_db)):
    """
    获取指定游戏的所有属性
    """
    attributes = attribute_crud.get_attributes_by_game(db, game_id)
    return attributes

@router.put("/{attribute_id}", response_model=AttributeUpdate)
def update_attribute(attribute_id: int, attribute: AttributeUpdate, db: Session = Depends(get_db)):
    """
    更新属性的初始值或名称（部分更新）
    """
    db_attr = db.query(PlayerAttribute).filter(PlayerAttribute.id == attribute_id).first()
    if not db_attr:
        raise HTTPException(status_code=404, detail="Attribute not found")

    # 使用 exclude_unset 过滤未传入的字段
    update_data = attribute.dict(exclude_unset=True)
    print(f"Update data: {update_data}")  # 调试输出实际更新的数据

    for key, value in update_data.items():
        setattr(db_attr, key, value)  # 动态更新字段

    db.commit()
    db.refresh(db_attr)
    return db_attr



@router.delete("/{attribute_id}")
def delete_attribute(attribute_id: int, db: Session = Depends(get_db)):
    success = attribute_crud.delete_attribute(db, attribute_id)
    if not success:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return {"ok": True}
