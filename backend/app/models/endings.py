from sqlalchemy import Column, Integer, Text, ForeignKey, JSON
from app.database import Base

class Ending(Base):
    __tablename__ = "endings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    description = Column(Text)
    trigger_conditions = Column(JSON)  # Example: [{"attribute": "strength", "condition": ">=", "value": 10}, {"attribute": "intelligence", "condition": "<", "value": 5}]
