from django.urls import path

from . import views
from .views import PostListView,PostDetailView,search

app_name = 'article'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('search/', search, name='search'),
    path('create/', views.create_post, name='create'),
path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]




