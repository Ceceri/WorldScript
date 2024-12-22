from pydantic import BaseModel
from typing import Optional, List, Any

class GameBase(BaseModel):
    title: str
    background: Optional[str]
    random_entries: Optional[List[Any]] = []

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    title: Optional[str]
    background: Optional[str]
    random_entries: Optional[List[Any]]

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True
