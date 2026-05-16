from django.db import models
from article.models import Category, Tag, Post

def sidebar_data(request):
    return {
        'categories': Category.objects.annotate(post_count=models.Count('posts')).filter(posts__isnull=False),
        'tags': Tag.objects.all(),
        'recent_posts': Post.objects.filter(status='published').order_by('-publish_time')[:5],
    }