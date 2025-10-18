from django.contrib import admin
from .models import Blog, Category, Tag

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'category', 'created_at')
	list_filter = ('category', 'tags')
	search_fields = ('title', 'author', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
