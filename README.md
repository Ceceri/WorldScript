This is a Gaming system based on LLM API
# WorldScript
  
一个基于LLM API接口的文字冒险游戏框架，提供了游玩和编辑游戏的功能，支持前后端联动和自定义配置。前端由HTML, CSS和JavaScript构成， 后端基于python和OpenAI API，数据库使用的是mysql

---

## **项目目录结构**
```plaintext
project/
├── backend/               # 后端代码
│   ├── app/
│   │   ├── core/          # 核心配置
│   │   ├── routers/       # 路由逻辑
│   │   ├── schemas/       # 数据模型
│   │   ├── utils/         # 实用工具
│   │   ├── models/        # 数据库模型
│   │   ├── crud/          # 数据库操作
│   │   ├── alembic/       # 数据库迁移
│   │   ├── main.py        # 主应用程序文件
│   │   ├── init_db.py     # 数据库初始化脚本
│   │   └── database.py    # 数据库连接配置
├── frontend/              # 前端代码
│   ├── css/               # 样式文件
│   ├── js/                # JavaScript 脚本
│   ├── images/            # 图片资源
│   ├── play_game.html     # 游戏页面HTML文件
│   ├── edit_game.html     # 编辑游戏页面HTML文件
│   └── index.html         # 主页HTML文件
├── .env                   # 环境变量文件（未被提交）
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明文件


配置环境：
进入项目目录
```bash
cd WorldScript
```
创建虚拟环境
```bash
python -m venv WS
```
激活虚拟环境
```bash
source WS/bin/activate
```
下载依赖
```bash
pip install -r requirements.txt
```

搭建MySQL数据库：
```bash
create database worldscript;
```
设置密钥：
在WorldScript目录下，创建.env文件，设置OPENAI_API_KEY和MYSQL_PASSWORD，如下所示
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/worldscript 
```

运行后端
```bash
cd backend
uvicorn app.main:app --reload
```
运行前端
```bash
cd frontend
python -m http.server 8001
```
然后就可以在浏览器中访问http://localhost:8001/index.html，开始编辑、游玩游戏

