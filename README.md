# MyBlog - 个人博客系统

一个基于 Django 6.0 构建的现代化个人博客系统，支持文章管理、嵌套评论、用户认证、AI 自动生成摘要、Redis 缓存、Docker 容器化部署等功能。

## ✨ 功能特性

### 核心功能
- **文章管理**：支持发布、编辑、删除文章，集成 CKEditor 富文本编辑器，支持代码高亮
- **分类与标签**：文章可分类管理，支持多标签
- **嵌套评论**：支持无限级嵌套评论（基于 MPTT），可展开/折叠子评论
- **用户认证**：注册、登录、登出功能
- **全文搜索**：基于标题和内容的全文搜索
- **AI 智能摘要**：接入 DeepSeek API，发布文章时自动生成摘要，无需手动填写

### 界面特性
- 响应式设计，适配各种设备
- 美观的卡片式布局，文章列表支持封面图
- 阅读量统计
- 侧边栏展示分类、标签云、最新文章
- Bootstrap 5 + Font Awesome 图标

### 技术特性
- CKEditor 富文本编辑器，支持代码块高亮
- MPTT 算法实现高效嵌套评论
- Redis 缓存（首页列表 + 侧边栏片段），提升访问速度
- 支持 SQLite（开发）/ MySQL（生产）
- **Docker 容器化部署**，一键启动全套服务（Django + MySQL + Redis + Nginx）

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| Django | 6.0.5 | Web 框架 |
| Django CKEditor | 6.7.0 | 富文本编辑器 |
| django-mptt | 0.14.0 | 嵌套模型支持 |
| django-redis | 5.4.0 | Redis 缓存后端 |
| Bootstrap | 5.3 | 前端样式框架 |
| Font Awesome | 6.x | 图标库 |
| MySQL | 8.0 | 生产数据库（可选） |
| Redis | 7.0 | 缓存 |
| Nginx | Alpine | 反向代理 + 静态文件服务 |
| Gunicorn | - | WSGI 服务器 |
| Docker | - | 容器化部署 |

## 📁 项目结构

```
MyBlog/
├── article/          # 文章模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py     # 文章、分类、标签模型
│   ├── signals.py    # AI 摘要生成信号
│   ├── urls.py       # 文章相关 URL
│   ├── views.py      # 文章视图
│   └── migrations/   # 数据库迁移
├── comment/          # 评论模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py     # 评论模型（MPTT 树形结构）
│   ├── urls.py
│   └── views.py
├── user/             # 用户模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py     # 自定义用户模型
│   ├── urls.py
│   └── views.py
├── MyBlog/           # 项目配置
│   ├── __init__.py
│   ├── asgi.py
│   ├── context_processors.py  # 全局上下文
│   ├── settings.py   # 项目设置（支持环境变量）
│   ├── urls.py       # 总路由
│   └── wsgi.py
├── templates/        # 模板文件
│   ├── article/      # 文章模板
│   ├── comment/      # 评论模板
│   ├── registration/ # 认证模板
│   └── base.html     # 基础模板
├── static/           # 静态文件（开发时）
├── media/            # 用户上传文件（头像、文章封面）
├── nginx/            # Nginx 配置文件
│   └── default.conf
├── Dockerfile        # Django 应用镜像
├── docker-compose.yml # 全套服务编排
├── .env.example      # 环境变量模板
├── requirements.txt
└── manage.py         # 管理命令
```

## 🚀 快速开始

### 方式一：使用 Docker（推荐，生产级）

#### 环境要求
- Docker (≥ 20.10)
- Docker Compose (≥ 2.0)

#### 一键启动
```bash
git clone <repository-url>
cd MyBlog
cp .env.example .env   # 可选：修改数据库密码等
docker-compose up -d
```
等待镜像构建完成后访问 http://localhost 即可。

#### 首次运行需创建超级管理员
```bash
docker-compose exec web python manage.py createsuperuser
```

#### 停止服务
```bash
docker-compose down
```

### 方式二：传统本地运行（开发调试）

#### 环境要求
- Python 3.10+
- Redis（可选，若不用可关闭缓存）
- MySQL（可选，默认使用 SQLite）

#### 步骤
1. **克隆项目**
```bash
git clone <repository-url>
cd MyBlog
```

2. **创建虚拟环境**
```bash
python -m venv .venv
```

3. **激活虚拟环境**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **安装依赖**
```bash
pip install -r requirements.txt
```

5. **配置环境变量**

复制 `.env.example` 为 `.env` 并修改配置：
```bash
cp .env.example .env
```

6. **数据库迁移**
```bash
python manage.py migrate
```

7. **创建超级用户**
```bash
python manage.py createsuperuser
```

8. **启动开发服务器**
```bash
python manage.py runserver
```

访问 http://localhost:8000 即可查看博客首页。

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_NAME` | 数据库名 | `myblog` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | 空（Docker 需指定） |
| `DB_HOST` | 数据库主机 | `localhost`（Docker 中为 `db`） |
| `DB_PORT` | 数据库端口 | `3306` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥（用于 AI 摘要） | 空（如不配置则不生成摘要） |
| `REDIS_HOST` | Redis 主机 | `localhost`（Docker 中为 `redis`） |
| `REDIS_PORT` | Redis 端口 | `6379` |

### 数据库切换

- 默认使用 SQLite（`db.sqlite3`）
- 如需使用 MySQL，设置 `.env` 中的数据库相关变量

### 缓存开关

缓存默认使用 Redis。若无 Redis 服务，可在 `settings.py` 中改为本地内存缓存：
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### CKEditor 代码高亮

已配置 `codesnippet` 插件，支持 Python、JavaScript、HTML、CSS、Bash、SQL。

## 📌 URL 路由

| URL | 视图 | 说明 |
|-----|------|------|
| `/` | 首页 | 文章列表（分页） |
| `/post/<slug>/` | 文章详情 | 查看文章 |
| `/create/` | 发布文章 | 登录后可用 |
| `/edit/<slug>/` | 编辑文章 | 仅作者可用 |
| `/delete/<slug>/` | 删除文章 | 仅作者可用 |
| `/my-posts/` | 我的文章 | 登录后可用 |
| `/search/?q=xxx` | 搜索 | 全文搜索 |
| `/accounts/login/` | 登录 | 用户登录 |
| `/accounts/register/` | 注册 | 用户注册 |
| `/accounts/logout/` | 登出 | 用户登出 |
| `/admin/` | 管理后台 | 管理员登录 |

## 📝 使用说明

### 发布文章
1. 登录后点击导航栏"发布文章"
2. 填写标题、正文（CKEditor 支持富文本）
3. 选择分类、输入标签（逗号分隔）
4. 可选上传封面图
5. 提交后自动生成摘要（若配置了 DeepSeek API）

### 嵌套评论
- 在文章详情页底部评论框输入评论内容为一级评论
- 点击某条评论下的"回复"按钮，可回复该评论
- 点击展开/折叠按钮查看/隐藏子评论

### 搜索文章
- 在导航栏搜索框输入关键词，支持标题和正文模糊匹配

## 🐳 Docker 生产部署说明

`docker-compose.yml` 编排了四个服务：
- `db`: MySQL 8
- `redis`: Redis 7 (Alpine)
- `web`: Django + Gunicorn
- `nginx`: Nginx 反向代理 + 静态/媒体文件服务

所有数据持久化存储于 Docker 卷中。生产环境建议修改 `.env` 中的强密码，并配置 `ALLOWED_HOSTS` 为你的域名。
