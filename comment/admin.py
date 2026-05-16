from django.contrib import admin
# 这是一个专门为树形模型（MPTTModel）设计的 Admin 类。
# 它能让你的评论列表以树状缩进的方式展示，并且每条记录前面有一个拖拽手柄，你可以通过拖拽来调整节点的层级和顺序（例如将一条子评论拖拽到另一条评论下，或改变同级评论的顺序）。
from mptt.admin import DraggableMPTTAdmin
from .models import Comment

# 将 Comment 模型注册到 Admin 后台，并使用 DraggableMPTTAdmin 作为它的管理界面。
# 如果不指定第二个参数，Django 会使用默认的 ModelAdmin。这里显式指定为 DraggableMPTTAdmin，就获得了树形拖拽能力。
admin.site.register(Comment, DraggableMPTTAdmin)