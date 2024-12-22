from sqlalchemy.orm import Session
from app.models.games import Game
from app.schemas.game_schemas import GameCreate, GameUpdate

def get_game(db: Session, game_id: int):
    return db.query(Game).filter(Game.id == game_id).first()

def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Game).offset(skip).limit(limit).all()

def create_game(db: Session, game: GameCreate):
    db_game = Game(
        title=game.title,
        background=game.background,
        random_entries=game.random_entries
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def update_game(db: Session, game_id: int, game: GameUpdate):
    db_game = get_game(db, game_id)
    if not db_game:
        return None
    if game.title is not None:
        db_game.title = game.title
    if game.background is not None:
        db_game.background = game.background
    if game.random_entries is not None:
        db_game.random_entries = game.random_entries
    db.commit()
    db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_id: int):
    db_game = get_game(db, game_id)
    if db_game:
        db.delete(db_game)
        db.commit()
        return True
    return False
