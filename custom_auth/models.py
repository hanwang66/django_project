
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	nickname = models.CharField(max_length=30, blank=True, verbose_name='昵称')
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
	bio = models.TextField(blank=True, verbose_name='简介')
	# 可扩展更多字段，如手机号等

	def __str__(self):
		return self.nickname or self.user.username
