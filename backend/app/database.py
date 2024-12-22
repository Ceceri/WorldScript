# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 测试数据库连接
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("数据库连接成功！")
    except Exception as e:
        print("数据库连接失败：", e)
