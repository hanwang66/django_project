from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=30, unique=True)
	def __str__(self):
		return self.name

class Blog(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=50)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
	tags = models.ManyToManyField(Tag, blank=True, related_name='blogs')

	def __str__(self):
		return self.title
