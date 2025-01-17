# WorldScript

<div id="language-selector">
  <button onclick="switchLanguage('zh')">中文</button>
  <button onclick="switchLanguage('en')">English</button>
</div>

<div id="content">
  <!-- 中文内容 -->
  <div id="zh" style="display: block;">
    ## 一个基于LLM API接口的文字冒险游戏框架

    WorldScript 是一个基于 LLM API 接口的文字冒险游戏框架，提供了游玩和编辑游戏的功能，支持前后端联动和自定义配置。前端由 HTML、CSS 和 JavaScript 构成，后端基于 Python 和 OpenAI API，数据库使用的是 MySQL。

    ### **项目目录结构**

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

    ### **配置环境**

    **1. 进入项目目录**
    ```bash
    cd WorldScript
    ```

    **2. 创建虚拟环境**
    ```bash
    python -m venv WS
    ```

    **3. 激活虚拟环境**
    ```bash
    source WS/bin/activate
    ```

    **4. 下载依赖**
    ```bash
    pip install -r requirements.txt
    ```

    ### **搭建MySQL数据库**

    **1. 创建数据库**
    ```bash
    create database worldscript;
    ```

    **2. 设置密钥**

    在 `WorldScript` 目录下，创建 `.env` 文件，设置 `OPENAI_API_KEY` 和 `MYSQL_PASSWORD`，内容如下：
    ```
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/worldscript 
    ```

    ### **运行项目**

    **1. 运行后端**
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```

    **2. 运行前端**
    ```bash
    cd frontend
    python -m http.server 8001
    ```

    在浏览器中访问：[http://localhost:8001/index.html](http://localhost:8001/index.html)
  </div>

  <!-- English Content -->
  <div id="en" style="display: none;">
    ## A Gaming System Based on LLM API

    WorldScript is a text-based adventure game framework built on the LLM API. It provides both gameplay and game editing functionality, supporting frontend-backend interaction and custom configuration. The frontend is built with HTML, CSS, and JavaScript, while the backend is powered by Python, OpenAI API, and MySQL as the database.

    ### **Project Directory Structure**

    ```plaintext
    project/
    ├── backend/               # Backend code
    │   ├── app/
    │   │   ├── core/          # Core configurations
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
    │   ├── css/               # Style files
    │   ├── js/                # JavaScript scripts
    │   ├── images/            # Image resources
    │   ├── play_game.html     # Game page HTML file
    │   ├── edit_game.html     # Game editing page HTML file
    │   └── index.html         # Homepage HTML file
    ├── .env                   # Environment variables file (not committed)
    ├── requirements.txt       # Python dependencies
    └── README.md              # Project description file
    ```

    ### **Setup Instructions**

    **1. Navigate to the project directory**
    ```bash
    cd WorldScript
    ```

    **2. Create a virtual environment**
    ```bash
    python -m venv WS
    ```

    **3. Activate the virtual environment**
    ```bash
    source WS/bin/activate
    ```

    **4. Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

    ### **Setup MySQL Database**

    **1. Create a database**
    ```bash
    create database worldscript;
    ```

    **2. Set up secrets**

    In the `WorldScript` directory, create a `.env` file and configure `OPENAI_API_KEY` and `MYSQL_PASSWORD` as shown:
    ```
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/worldscript 
    ```

    ### **Run the Application**

    **1. Run the backend**
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```

    **2. Run the frontend**
    ```bash
    cd frontend
    python -m http.server 8001
    ```

    Access the application in your browser at: [http://localhost:8001/index.html](http://localhost:8001/index.html)
  </div>
</div>

<script>
function switchLanguage(lang) {
  document.getElementById('zh').style.display = lang === 'zh' ? 'block' : 'none';
  document.getElementById('en').style.display = lang === 'en' ? 'block' : 'none';
}
</script>
