from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from app.database import Base

class GameEvent(Base):
    __tablename__ = "game_events"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    range_condition = Column(JSON, nullable=True) # 如 {"attribute": "date", "min":5, "max":10}
