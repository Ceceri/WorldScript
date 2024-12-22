# backend/app/main.py

from fastapi import FastAPI
from app.routers import games, events, options, attributes, endings, llm
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from fastapi.staticfiles import StaticFiles


# 导入所有模型以确保 SQLAlchemy 识别它们
from app.models.games import Game
from app.models.events import GameEvent
from app.models.options import GameOption
from app.models.attributes import PlayerAttribute
from app.models.endings import Ending
from fastapi import APIRouter
from app.core.config import settings

# 加载环境变量
load_dotenv()

# 创建 FastAPI 实例
app = FastAPI(title="Game Narrative System")



# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境用）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

debug_router = APIRouter()
@debug_router.get("/debug_api_key")
def debug_api_key():
    return {"OPENAI_API_KEY": settings.OPENAI_API_KEY}

app.include_router(debug_router)

# 包含所有路由
app.include_router(games.router)
app.include_router(events.router)
app.include_router(options.router)
app.include_router(attributes.router)
app.include_router(endings.router)
app.include_router(llm.router)

# 导入 Base 和 engine 以创建表
from app.database import Base, engine

# 创建所有表（如果不存在）
Base.metadata.create_all(bind=engine)
