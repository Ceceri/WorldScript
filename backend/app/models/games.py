from sqlalchemy import Column, Integer, String, Text, JSON
from app.database import Base

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    background = Column(Text)
    random_entries = Column(JSON)  # [{"entry":"你是一位商人","attributes":{"wealth":10}}, ...]
