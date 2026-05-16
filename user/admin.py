from django.contrib import admin
# 导入 Django 默认的 UserAdmin 类，它已经为用户名、密码、权限、组等字段配置好了后台管理界面（包括列表显示、筛选、搜索、添加/编辑表单等）。
from django.contrib.auth.admin import UserAdmin
from .models import User # 从当前应用（user）的 models.py 中导入我们自定义的 User 模型。

# 注册自定义 User 模型，并直接使用 Django 内置的 UserAdmin
admin.site.register(User, UserAdmin)
# 将自定义的 User 模型注册到后台，并使用 UserAdmin 来管理它。这样，Django Admin 后台会以标准的用户管理样式显示我们扩展后的用户模型（自动包含 bio 和 avatar 字段，因为 UserAdmin 会识别模型上的所有字段，但有时你可能需要自定义 fieldsets 来将新字段放到合适的位置）。