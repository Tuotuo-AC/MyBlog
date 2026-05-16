from django.db import models
from django.contrib.auth.models import AbstractUser
# AbstractUser 是 Django 提供的可扩展的用户模型基类，它已经包含了默认用户模型的所有字段（如 username、password、email、first_name、last_name 等）和方法（如 authenticate、has_perm 等）。

# 继承自AbstractUser, User 模型将拥有 Django 默认用户模型的所有功能，同时我们还可以在此基础上添加额外的字段或方法。
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    # 用于上传用户头像
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # 这是 Python 对象的标准字符串表示方法。
    # 当我们在 Admin 后台或打印用户对象时，会返回用户的 username 字段，而不是类似于 <User: User object (1)> 这样的默认输出。
    def __str__(self):
        return self.username

