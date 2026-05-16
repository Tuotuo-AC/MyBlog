from django.urls import path
from .views import PostListView,PostDetailView,search

app_name = 'article'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('search/', search, name='search'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]




