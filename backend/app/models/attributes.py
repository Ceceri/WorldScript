from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class PlayerAttribute(Base):
    __tablename__ = "player_attributes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    name = Column(String(50), nullable=False)
    initial_value = Column(Float, default=0.0)
