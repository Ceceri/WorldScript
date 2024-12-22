from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.ending_schemas import Ending, EndingCreate, EndingUpdate
from app.crud import ending_crud

router = APIRouter(prefix="/endings", tags=["endings"])

@router.post("/", response_model=Ending)
def create_new_ending(ending: EndingCreate, db: Session = Depends(get_db)):
    return ending_crud.create_ending(db, ending)

@router.get("/{ending_id}", response_model=Ending)
def read_ending(ending_id: int, db: Session = Depends(get_db)):
    db_end = ending_crud.get_ending(db, ending_id)
    if not db_end:
        raise HTTPException(status_code=404, detail="Ending not found")
    return db_end

@router.put("/{ending_id}", response_model=Ending)
def update_ending(ending_id: int, ending: EndingUpdate, db: Session = Depends(get_db)):
    db_end = ending_crud.update_ending(db, ending_id, ending)
    if not db_end:
        raise HTTPException(status_code=404, detail="Ending not found")
    return db_end

@router.delete("/{ending_id}")
def delete_ending(ending_id: int, db: Session = Depends(get_db)):
    success = ending_crud.delete_ending(db, ending_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ending not found")
    return {"ok": True}

@router.get("/", response_model=list[Ending])
def read_endings(game_id: int, db: Session = Depends(get_db)):
    """
    查询指定 game_id 的所有结局
    """
    endings = ending_crud.get_endings_by_game(db, game_id)
    if not endings:
        raise HTTPException(status_code=404, detail="No endings found for this game")
    return endings
