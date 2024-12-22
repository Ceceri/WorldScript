from app.database import Base, engine
from app.models.games import Game  # 导入所有模型

# 删除并重新创建所有表
Base.metadata.drop_all(bind=engine)  # 删除所有表（可选）
Base.metadata.create_all(bind=engine)  # 创建所有表

print("数据库表已初始化！")
