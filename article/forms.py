from django import forms
from .models import Post, Category, Tag
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    # content 使用 CKEditor 小部件，使前台也能富文本编辑
    content = forms.CharField(widget=CKEditorWidget(), label='正文')
    # 标签暂时以逗号分隔字符串处理，后面在视图中创建或获取 Tag 对象。
    tags = forms.CharField(required=False, help_text='多个标签用逗号分隔', label='标签')

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['status'].initial = 'published'  # 默认已发布

    def clean_tags(self):
        tag_str = self.cleaned_data.get('tags')
        if not tag_str:
            return []
        tags = [t.strip() for t in tag_str.split(',') if t.strip()]
        return tags