from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.option_schemas import Option, OptionCreate, OptionUpdate
from app.crud import option_crud

router = APIRouter(prefix="/options", tags=["options"])

@router.post("/", response_model=Option)
def create_new_option(option: OptionCreate, db: Session = Depends(get_db)):
    return option_crud.create_option(db, option)

@router.get("/", response_model=List[Option])
def read_options_by_event(event_id: str = Query(None), db: Session = Depends(get_db)):
    if event_id:
        # 如果有event_id，则返回该事件下的所有选项
        return option_crud.get_options_by_event(db, event_id)
    else:
        # 如果没有event_id参数，根据需求可返回空列表或者其他处理方式
        return []
    
@router.get("/{option_id}", response_model=Option)
def read_option(option_id: int, db: Session = Depends(get_db)):
    db_option = option_crud.get_option(db, option_id)
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    return db_option

@router.put("/{option_id}", response_model=Option)
def update_option(option_id: int, option: OptionUpdate, db: Session = Depends(get_db)):
    db_option = option_crud.update_option(db, option_id, option)
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    return db_option

@router.delete("/{option_id}")
def delete_option(option_id: int, db: Session = Depends(get_db)):
    success = option_crud.delete_option(db, option_id)
    if not success:
        raise HTTPException(status_code=404, detail="Option not found")
    return {"ok": True}
