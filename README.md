# MyBlog - 个人博客系统

一个基于 Django 6.0 构建的现代化个人博客系统（MySQL + Bootstrap + ckeditor + Agent），支持文章管理、嵌套评论、用户认证等功能。

## ✨ 功能特性

### 核心功能
- **文章管理**：支持发布、编辑、删除文章，支持富文本编辑器
- **分类与标签**：文章可分类管理，支持多标签
- **嵌套评论**：支持无限级嵌套评论，可展开/折叠子评论
- **用户认证**：注册、登录、登出功能
- **搜索功能**：支持文章标题搜索

### 界面特性
- 响应式设计，适配各种设备
- 美观的卡片式布局
- 文章摘要支持留空由AI生成
- 阅读量统计
- 侧边栏展示分类、标签云、最新文章

### 技术特性
- 使用 CKEditor 富文本编辑器
- MPTT 实现嵌套评论
- Redis 缓存支持
- SQLite/MySQL 数据库支持

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| Django | 6.0.5 | Web 框架 |
| Django CKEditor | 6.7.0 | 富文本编辑器 |
| django-mptt | 0.14.0 | 嵌套模型支持 |
| django-redis | 5.4.0 | Redis 缓存 |
| Bootstrap | 5.3 | 前端框架 |
| Font Awesome | 6.x | 图标库 |

## 📁 项目结构

```
MyBlog/
├── article/          # 文章模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py     # 文章、分类、标签模型
│   ├── urls.py       # 文章相关 URL
│   ├── views.py      # 文章视图
│   └── migrations/   # 数据库迁移
├── comment/          # 评论模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py     # 评论模型（支持嵌套）
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
│   ├── settings.py   # 项目设置
│   ├── urls.py       # 总路由
│   └── wsgi.py
├── templates/        # 模板文件
│   ├── article/      # 文章模板
│   ├── comment/      # 评论模板
│   ├── registration/ # 认证模板
│   └── base.html     # 基础模板
├── static/           # 静态文件
├── media/            # 媒体文件
├── .env              # 环境变量
├── .env.example      # 环境变量示例
├── manage.py         # 管理命令
└── README.md         # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Redis (可选，用于缓存)
- MySQL (可选，默认使用 SQLite)

### 安装步骤

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

编辑 `.env` 文件：
```env
DB_NAME=myblog
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
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

### 数据库配置

默认使用 SQLite，如需使用 MySQL，修改 `MyBlog/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}
```

### CKEditor 配置

CKEditor 已配置支持代码高亮，支持语言：Python、JavaScript、HTML、CSS、Bash、SQL。

### 缓存配置

默认使用 Redis 缓存，如需禁用缓存，修改 `MyBlog/settings.py`：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

## 📌 URL 路由

| URL | 视图 | 说明 |
|-----|------|------|
| `/` | 首页 | 文章列表 |
| `/post/<slug>/` | 文章详情 | 查看文章 |
| `/create/` | 发布文章 | 登录后可用 |
| `/edit/<slug>/` | 编辑文章 | 仅作者可用 |
| `/delete/<slug>/` | 删除文章 | 仅作者可用 |
| `/my-posts/` | 我的文章 | 登录后可用 |
| `/search/?q=xxx` | 搜索 | 搜索文章 |
| `/accounts/login/` | 登录 | 用户登录 |
| `/accounts/register/` | 注册 | 用户注册 |
| `/accounts/logout/` | 登出 | 用户登出 |
| `/admin/` | 管理后台 | 管理员登录 |

## 📝 使用说明

### 发布文章

1. 登录后点击导航栏"发布文章"
2. 填写标题、正文内容
3. 选择分类和标签
4. 可选上传封面图片
5. 点击"发布"按钮

### 评论功能

1. 在文章详情页底部评论框输入评论内容
2. 点击"回复"按钮回复特定评论
3. 点击展开/折叠按钮查看/隐藏子评论

### 搜索文章

1. 在导航栏搜索框输入关键词
2. 点击搜索按钮或按回车

