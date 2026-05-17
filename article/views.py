# ListView用于展示对象列表（如文章列表页），DetailView用于展示单个对象详情（如文章详情页）
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404 # 根据条件获取对象，找不到则自动返回 404 页面
from .models import Post
from django.utils.text import slugify
from comment.models import Comment
from comment.forms import CommentForm

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

    # 将评论表单和评论列表传递给模板供渲染
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_html'] = self.object.content  # ckeditor 输出已是 HTML
        context['comment_form'] = CommentForm()
        # 获取所有评论，使用 recursetree 标签自动处理树形结构
        context['comments'] = self.object.comments.all()
        return context

    # 处理表单提交:验证、保存评论、关联文章和当前用户，支持嵌套评论（通过parent_id)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user

            # 处理回复逻辑
            # 如果有 parent_id 参数，说明是回复评论
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                    # 关键：设置 reply_to 为被回复的用户
                    comment.reply_to = parent_comment.author
                except Comment.DoesNotExist:
                    pass
            else:
                comment.parent = None
                comment.reply_to = None

            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils import timezone
from .forms import PostForm
from .models import Tag
import time

# 只有登录用户可访问
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # ... 前面代码不变
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published'
            post.publish_time = timezone.now()
            # 生成slug
            base_slug = slugify(post.title)
            if not base_slug:
                base_slug = f"post-{int(time.time())}"
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug

            post.save()  # 先保存文章，才能设置多对多标签

            # 处理标签
            tags = form.cleaned_data.get('tags', [])
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name, slug=slugify(tag_name))
                post.tags.add(tag)

            return redirect('article:detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'article/create.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # 权限检查：只能编辑自己的文章
    if post.author != request.user:
        return redirect('article:detail', slug=post.slug)  # 或者返回 403 页面
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            # 如果标题修改了，需要重新生成 slug（可选）
            if updated_post.title != post.title:
                base_slug = slugify(updated_post.title)
                if not base_slug:
                    base_slug = f"post-{int(time.time())}"
                new_slug = base_slug
                counter = 1
                while Post.objects.filter(slug=new_slug).exclude(pk=post.pk).exists():
                    new_slug = f"{base_slug}-{counter}"
                    counter += 1
                updated_post.slug = new_slug
            updated_post.save()
            # 处理标签（如果有表单字段）
            tags = form.cleaned_data.get('tags', [])
            if tags:
                updated_post.tags.clear()
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name, slug=slugify(tag_name))
                    updated_post.tags.add(tag)
            return redirect('article:detail', slug=updated_post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'article/edit.html', {'form': form, 'post': post})


@login_required
def my_posts(request):
    posts_list = Post.objects.filter(author=request.user).order_by('-publish_time')
    paginator = Paginator(posts_list, 10) # 每页10篇
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article/my_posts.html',{'page_obj':page_obj})


from django.contrib import messages
@login_required
# 删除功能通常需要俩个步骤：显示确认删除页面（GET请求）和实际执行删除（POST请求）
def delete_post(request, slug):
    # 通过slug获取文章，检查作者是否为当前用户，否则拒绝并提示
    post = get_object_or_404(Post, slug=slug)
    # 检查权限，只有作者可以删除
    if post.author != request.user:
        messages.error(request,'您没有权限可以删除此文章')
        return redirect('article:detail', slug=post.slug)

    # 执行删除，成功后通过messages框架显示提示，并重定向到我的文章列表
    if request.method == 'POST':
        # 确认删除
        post_title = post.title
        post.delete()
        messages.success(request,f'文章《{post_title}》已成功删除。')
        return redirect('article:my_posts')

    # GET请求时渲染确认删除模板
    return render(request,'article/confirm_delete.html',{'post':post})
