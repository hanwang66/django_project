from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Category, Tag, Comment
from django.http import HttpResponse

def blog_index(request):
	blogs = Blog.objects.all().order_by('-created_at')
	return render(request, "blog/list_blog.html", {"blogs": blogs})

def blog_detail(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	comments = Comment.objects.filter(blog=blog, parent=None, is_approved=True).order_by('-created_at')
	if request.method == "POST":
		user = request.POST.get("user", "匿名")
		content = request.POST.get("content", "")
		parent_id = request.POST.get("parent_id")
		parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
		# 简单敏感词过滤
		sensitive_words = ["傻逼", "垃圾", "fuck"]
		has_sensitive = any(word in content for word in sensitive_words)
		comment = Comment.objects.create(
			blog=blog, user=user, content=content, parent=parent,
			is_approved=not has_sensitive, has_sensitive=has_sensitive
		)
		return redirect(f"/blog/{pk}/")
	return render(request, "blog/blog_detail.html", {"blog": blog, "comments": comments})

	blog = get_object_or_404(Blog, pk=pk)
	comments = Comment.objects.filter(blog=blog, parent=None, is_approved=True).order_by('-created_at')
	if request.method == "POST":
		user = request.POST.get("user", "匿名")
		content = request.POST.get("content", "")
		parent_id = request.POST.get("parent_id")
		parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
		# 简单敏感词过滤
		sensitive_words = ["傻逼", "垃圾", "fuck"]
		has_sensitive = any(word in content for word in sensitive_words)
		comment = Comment.objects.create(
			blog=blog, user=user, content=content, parent=parent,
			is_approved=not has_sensitive, has_sensitive=has_sensitive
		)
		return redirect(f"/blog/{pk}/")
	return render(request, "blog/blog_detail.html", {"blog": blog, "comments": comments})

def blog_add(request):
	categories = Category.objects.all()
	tags = Tag.objects.all()
	if request.method == "POST":
		title = request.POST.get("title")
		author = request.POST.get("author")
		content = request.POST.get("content")
		category_id = request.POST.get("category")
		tag_ids = request.POST.getlist("tags")
		category = Category.objects.filter(id=category_id).first() if category_id else None
		blog = Blog.objects.create(title=title, author=author, content=content, category=category)
		if tag_ids:
			blog.tags.set(Tag.objects.filter(id__in=tag_ids))
		return redirect("/blog/")
	return render(request, "blog/add_blog.html", {"categories": categories, "tags": tags})

def blog_edit(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	categories = Category.objects.all()
	tags = Tag.objects.all()
	if request.method == "POST":
		blog.title = request.POST.get("title")
		blog.author = request.POST.get("author")
		blog.content = request.POST.get("content")
		category_id = request.POST.get("category")
		tag_ids = request.POST.getlist("tags")
		blog.category = Category.objects.filter(id=category_id).first() if category_id else None
		blog.save()
		if tag_ids:
			blog.tags.set(Tag.objects.filter(id__in=tag_ids))
		else:
			blog.tags.clear()
		return redirect(f"/blog/{pk}/")
	return render(request, "blog/edit_blog.html", {"blog": blog, "categories": categories, "tags": tags})

def blog_delete(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	if request.method == "POST":
		blog.delete()
		return redirect("/blog/")
	return render(request, "blog/delete_blog.html", {"blog": blog})
