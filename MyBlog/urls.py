"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('article.urls')),
       path('accounts/', include('django.contrib.auth.urls')),
       path('accounts/register/', register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 媒体文件服务（开发环境）
if settings.DEBUG:
    # 是开发环境下为了让 Django 提供用户上传文件访问的能力。
    # 这行代码不是必须的，但如果你希望在上传图片后立即能在浏览器中看到，就需要它。
    # 生产环境务必移除这行，改用 Web 服务器直接托管媒体文件。
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 如果你希望显式提供静态文件服务（通常不需要，Django 会自动处理），可以添加下面一行：
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)