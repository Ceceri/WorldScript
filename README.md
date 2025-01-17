# WorldScript

## A Gaming System Based on LLM API

WorldScript is a text adventure game framework based on the LLM API. It provides features for playing and editing games, supports front-end and back-end interaction, and allows custom configurations. The front end is built with HTML, CSS, and JavaScript, while the back end is developed using Python and OpenAI API, with MySQL as the database.

---

## **Project Directory Structure**

```plaintext
project/
├── backend/               # Backend code
│   ├── app/
│   │   ├── core/          # Core configuration
│   │   ├── routers/       # Routing logic
│   │   ├── schemas/       # Data models
│   │   ├── utils/         # Utility tools
│   │   ├── models/        # Database models
│   │   ├── crud/          # Database operations
│   │   ├── alembic/       # Database migrations
│   │   ├── main.py        # Main application file
│   │   ├── init_db.py     # Database initialization script
│   │   └── database.py    # Database connection configuration
├── frontend/              # Frontend code
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript scripts
│   ├── images/            # Image assets
│   ├── play_game.html     # Game page HTML file
│   ├── edit_game.html     # Game editing page HTML file
│   └── index.html         # Homepage HTML file
├── .env                   # Environment variable file (not included in version control)
├── requirements.txt       # Python dependencies
└── README.md              # Project description file
```

---

## Setting Up the Environment

Navigate to the project directory:
```bash
cd WorldScript
```

Create a virtual environment:
```bash
python -m venv WS
```

Activate the virtual environment:
```bash
source WS/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Setting Up the MySQL Database

Create the database:
```bash
create database worldscript;
```

Set up environment variables:  
In the `WorldScript` directory, create a `.env` file and set `OPENAI_API_KEY` and `MYSQL_PASSWORD`, as shown below:
```bash
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/worldscript 
```

---

## Running the Backend

Navigate to the backend directory:
```bash
cd backend
```

Start the backend server:
```bash
uvicorn app.main:app --reload
```

---

## Running the Frontend

Navigate to the frontend directory:
```bash
cd frontend
```

Start the frontend server:
```bash
python -m http.server 8001
```

Access the application in your browser at:
[http://localhost:8001/index.html](http://localhost:8001/index.html)

---

# WorldScript

## 基于LLM API的游戏系统

WorldScript 是一个基于 LLM API 的文字冒险游戏框架，提供了游玩和编辑游戏的功能，支持前后端联动和自定义配置。前端由 HTML、CSS 和 JavaScript 构成，后端基于 Python 和 OpenAI API，数据库使用的是 MySQL。

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
│   ├── play_game.html     # 游戏页面 HTML 文件
│   ├── edit_game.html     # 编辑游戏页面 HTML 文件
│   └── index.html         # 主页 HTML 文件
├── .env                   # 环境变量文件（未被提交）
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明文件
```

---

## 配置环境

进入项目目录：
```bash
cd WorldScript
```

创建虚拟环境：
```bash
python -m venv WS
```

激活虚拟环境：
```bash
source WS/bin/activate
```

下载依赖：
```bash
pip install -r requirements.txt
```

---

## 搭建 MySQL 数据库

创建数据库：
```bash
create database worldscript;
```

设置密钥：  
在 `WorldScript` 目录下，创建 `.env` 文件，设置 `OPENAI_API_KEY` 和 `MYSQL_PASSWORD`，如下所示：
```bash
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/worldscript 
```

---

## 运行后端

进入后端目录：
```bash
cd backend
```

启动后端服务：
```bash
uvicorn app.main:app --reload
```

---

## 运行前端

进入前端目录：
```bash
cd frontend
```

启动前端服务：
```bash
python -m http.server 8001
```

然后在浏览器中访问：
[http://localhost:8001/index.html](http://localhost:8001/index.html)
