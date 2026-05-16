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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from comment.forms import CommentForm

# 详情视图
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'article/detail.html'
    context_object_name = 'post'
    login_url = '/accounts/login/' # 未登录时跳转的地址

    # DetailView 默认的 get_object() 方法只处理 pk 或 slug。我们要改成：从 self.kwargs 中取出 year, month, day, slug，然后用这些条件去数据库查询
    def get_object(self,queryset=None):
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

    # 将评论表单和顶级评论列表传递给模板供渲染
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_html'] = self.object.content  # ckeditor 输出已是 HTML
        context['comment_form'] = CommentForm()
        # 获取顶级评论（parent 为 None）
        context['comments'] = self.object.comments.filter(parent=None)
        return context

    # 处理表单提交:验证、保存评论、关联文章和当前用户，支持嵌套评论（通过parent_id)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            # 如果有 parent_id 参数，说明是回复评论
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            return redirect(self.object.get_absolute_url())
        # 表单验证失败时重新渲染页面并显示错误
        return self.render_to_response(self.get_context_data(comment_form=form))

from django.db.models import Q
from django.shortcuts import render
# 搜索视图
def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )
    return render(request, 'article/search.html', {'results': results, 'query': query})




