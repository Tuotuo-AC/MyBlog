# 导入Django的数据库模型基类
from django.db import models
# 获取当前项目中配置的用户模型（自定义的 user.User），用于外键关联评论作者。
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey
# 导入文章模型，表示评论属于哪一篇文章
from article.models import Post

# 将自定义用户模型赋值给User变量方便使用
User = get_user_model()

# Comment 模型不继承普通的 models.Model，而是继承 MPTTModel。MPTTModel 自动为模型添加三个额外的字段：lft、rght、tree_id，用于存储树形结构信息。这样就可以通过 parent 字段轻松实现无限级嵌套评论。
class Comment(MPTTModel):
    # post 一条评论属于哪一篇文章，当文章被删除时，评论也一并删除
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # 评论的作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 评论的正文内容
    content = models.TextField(max_length=1000)
    # 评论创建时间。auto_now_add=True 表示对象第一次保存时自动设置为当前时间，之后不再更改。
    created = models.DateTimeField(auto_now_add=True)
    # 用于嵌套，指向父评论。如果一条评论是回复另一条评论，parent 就指向被回复的那条评论；如果是顶级评论（直接回复文章），则 parent = None。
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        # 当从数据库查询评论时，默认按 created 升序排列（最早的评论在前）。如果希望最新评论在前，可以改为 ['-created']
        ordering = ['created']

    def __str__(self):
        # 在 Admin 后台或打印对象时，返回易读的字符串表示，例如 “张三 评论 Django入门”，方便调试和管理。
        return f'{self.author} 评论 {self.post.title}'
