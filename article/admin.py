# 自定义 Django Admin 后台的显示和管理行为，让博客的分类、标签、文章更容易通过后台管理。

from django.contrib import admin # 导入 Django 内置的 admin 模块，它提供后台管理功能。
from .models import Category, Tag, Post # 从当前目录的 models.py 中导入我们定义的三个模型。

@admin.register(Category) # 当你在 Admin 后台管理 Category 模型时，使用后面定义的 CategoryAdmin 配置类，而不是默认的管理界面。
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'created_date')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'category', 'status', 'publish_time', 'views')
    list_filter = ('status', 'category', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)