def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('/')
		else:
			return render(request, 'auth/login.html', {'error': '用户名或密码错误'})
	return render(request, 'auth/login.html')

def register_view(request):
	from django.contrib.auth.models import User
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		if User.objects.filter(username=username).exists():
			return render(request, 'auth/register.html', {'error': '用户名已存在'})
		user = User.objects.create_user(username=username, password=password, email=email)
		login(request, user)
		return redirect('/')
	return render(request, 'auth/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
def logout_view(request):
	auth_logout(request)
	return redirect('/auth/login/')
from django.http import HttpResponse
from .models import Profile

@login_required
def profile_view(request):
	user = request.user
	profile, created = Profile.objects.get_or_create(user=user)
	if request.method == 'POST':
		# 判断是更换头像还是资料修改
		if 'change_avatar' in request.POST:
			avatar = request.FILES.get('avatar')
			if avatar:
				profile.avatar = avatar
				profile.save()
			return redirect('/profile/')
		else:
			nickname = request.POST.get('nickname', '').strip()
			bio = request.POST.get('bio', '').strip()
			email = request.POST.get('email', '').strip()
			profile.nickname = nickname
			profile.bio = bio
			profile.save()
			if email:
				user.email = email
				user.save()
			return redirect('/profile/')
	return render(request, 'auth/profile.html', {
		'user': user,
		'profile': profile,
	})
