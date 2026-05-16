# ListView用于展示对象列表（如文章列表页），DetailView用于展示单个对象详情（如文章详情页）
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404 # 根据条件获取对象，找不到则自动返回 404 页面
from .models import Post

# 列表视图
class PostListView(ListView):
    model = Post # 告诉ListView使用Post模型
    template_name = 'article/list.html' # 指定渲染模板路径
    context_object_name = 'posts' # 模板中使用的变量名
    paginate_by = 10 # 每页显示10篇文章，ListView会自动处理分页逻辑

    # 返回要展示的数据集（默认是 Model.objects.all()）。这里我们覆盖它，只筛选已发布的文章，并用 select_related 预先连表取出 author 和 category，避免 N+1 查询。
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author','category')

# 详情视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'article/detail.html'
    context_object_name = 'post'

    # DetailView 默认的 get_object() 方法只处理 pk 或 slug。我们要改成：从 self.kwargs 中取出 year, month, day, slug，然后用这些条件去数据库查询
    def get_object(self,queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(
            Post,
            slug=slug,
            status='published'
        )
        # 添加阅读量
        obj.views += 1
        obj.save(update_fields=['views']) # 只更新这个字段
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_html'] = self.object.content  # ckeditor 输出已是 HTML
        return context






