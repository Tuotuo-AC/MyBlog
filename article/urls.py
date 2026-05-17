from django.urls import path

from . import views
from .views import PostListView,PostDetailView,search

app_name = 'article'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('search/', search, name='search'),
    path('create/', views.create_post, name='create'),
    path('edit/<slug:slug>/', views.edit_post, name='edit'),
    path('my_posts/',views.my_posts,name='my_posts'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]




