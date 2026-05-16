from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from .forms import UserRegistrationForm   # 待创建

# 注册视图
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 注册后自动登录
            login(request, user)
            return redirect(reverse('article:list'))
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})