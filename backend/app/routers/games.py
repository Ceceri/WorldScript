# backend/app/routers/games.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.game_schemas import Game, GameCreate, GameUpdate
from app.crud import game_crud
import logging

router = APIRouter(prefix="/games", tags=["games"])

# 配置日志记录
logger = logging.getLogger("games_router")
logging.basicConfig(level=logging.INFO)

@router.get("/", response_model=List[Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        games = game_crud.get_games(db, skip=skip, limit=limit)
        return games
    except Exception as e:
        logger.error(f"Error fetching games: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/", response_model=Game)
def create_new_game(game: GameCreate, db: Session = Depends(get_db)):
    try:
        return game_crud.create_game(db, game)
    except Exception as e:
        logger.error(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{game_id}", response_model=Game)
def read_game(game_id: int, db: Session = Depends(get_db)):
    try:
        db_game = game_crud.get_game(db, game_id)
        if not db_game:
            raise HTTPException(status_code=404, detail="Game not found")
        return db_game
    except Exception as e:
        logger.error(f"Error fetching game {game_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{game_id}", response_model=Game)
def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    try:
        db_game = game_crud.update_game(db, game_id, game)
        if not db_game:
            raise HTTPException(status_code=404, detail="Game not found")
        return db_game
    except Exception as e:
        logger.error(f"Error updating game {game_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    try:
        success = game_crud.delete_game(db, game_id)
        if not success:
            raise HTTPException(status_code=404, detail="Game not found")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error deleting game {game_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
