from django import forms
from .models import Comment

# ModelForm 是 Django 提供的一种特殊表单类，它可以根据一个已有的模型自动生成表单字段，并能通过 save() 方法直接保存到数据库。
# 对比普通的 forms.Form，你需要手动定义每个字段。使用 ModelForm 可以避免重复定义（因为模型的字段已经定义了类型、长度、是否为空等属性）。
class CommentForm(forms.ModelForm):
    # 内部类用于提供元数据，告诉ModelForm如何基于模型生成表单
    class Meta:
        # 指定这个表单关联的模型是 Comment。Django 会读取 Comment 模型的字段定义，并自动为这些字段创建对应的表单字段。
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': '写下你的评论...'}),
        }