from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name='分类名')
    slug = models.SlugField(max_length=50, unique=True,verbose_name='url别名')
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural = 'Categories' # Admin中显示为复数

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名')
    slug = models.SlugField(max_length=40, unique=True, verbose_name='URL别名')

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    # 基本信息
    title = models.CharField(max_length=200, verbose_name='标题')
    #  unique_for_date='publish_time'：确保同一天发布的文章 slug 不重复，防止 URL 冲突。
    slug = models.SlugField(max_length=200, unique_for_date='publish_time', verbose_name='URL别名')

    # 作者（先使用 Django 内置的 User 模型）
    # author 字段：使用了 get_user_model()，它会返回当前项目配置的用户模型（默认是 auth.User）。这样即使以后换成自定义用户模型，也不用修改这行代码。
    author = models.ForeignKey(
        get_user_model(),  # 获取当前用户模型（默认是 auth.User）
        on_delete=models.CASCADE, # 当用户被删除时，他的文章也会被删除
        related_name='posts',
        verbose_name='作者'
    )

    # 关联分类和标签
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # 表示当分类被删除时，文章的分类字段设为 NULL（文章依然存在）。
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='分类'
    )
    # 使用多对多，一篇文章可以有多个标签。
    tags = models.ManyToManyField(
        'Tag',  # 或 Tag
        blank=True,
        related_name='posts',
        verbose_name='标签'
    )

    # 内容相关
    summary = models.CharField(max_length=300, blank=True,null=True, verbose_name='摘要', help_text='可留空由AI生成')
    content = RichTextField(verbose_name='正文', config_name='default')

    # 发布状态与时间
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='发布时间')

    # 自动记录
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 统计
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    # 添加图片字段
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='封面图')

    class Meta:
        ordering = ('-publish_time',)  # 按发布时间倒序

    def __str__(self):
        return self.title

    # 返回文章的详情页URL
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article:detail', args=[self.slug])