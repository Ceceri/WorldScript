from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey
from app.database import Base

class GameOption(Base):
    __tablename__ = "game_options"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    result_attribute_changes = Column(JSON, nullable=True)
    triggers_ending = Column(Boolean, default=False)
    ending_description = Column(String(255), nullable=True)
    event_id = Column(Integer, ForeignKey("game_events.id"), nullable=False)
    impact_description = Column(Text, nullable=True)  # 确保定义与数据库一致
