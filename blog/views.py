from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Category, Tag, Comment
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def blog_index(request):
	blogs = Blog.objects.all().order_by('-created_at')
	return render(request, "blog/list_blog.html", {"blogs": blogs})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def blog_detail(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	comments = Comment.objects.filter(blog=blog, parent=None, is_approved=True).order_by('-created_at')
	if request.method == "POST":
		if request.POST.get("like_comment_id"):
			comment_id = request.POST.get("like_comment_id")
			comment = Comment.objects.filter(id=comment_id).first()
			if comment:
				comment.likes += 1
				comment.save()
			return redirect(f"/blog/{pk}/")
		# 评论编辑
		if request.POST.get("edit_comment_id"):
			comment_id = request.POST.get("edit_comment_id")
			comment = Comment.objects.filter(id=comment_id).first()
			if comment and (request.user.is_superuser or (request.user.is_authenticated and comment.user == request.user.username)):
				new_content = request.POST.get("edit_content", "")
				comment.content = new_content
				comment.save()
			return redirect(f"/blog/{pk}/")
		# 评论删除
		if request.POST.get("delete_comment_id"):
			comment_id = request.POST.get("delete_comment_id")
			comment = Comment.objects.filter(id=comment_id).first()
			if comment and (request.user.is_superuser or (request.user.is_authenticated and comment.user == request.user.username)):
				comment.delete()
			return redirect(f"/blog/{pk}/")
		user = request.user.username if request.user.is_authenticated else "匿名"
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

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def blog_add(request):
	categories = Category.objects.all()
	tags = Tag.objects.all()
	if request.method == "POST":
		title = request.POST.get("title")
		# 强制使用当前登录用户名
		author = request.user.username if request.user.is_authenticated else "匿名"
		content = request.POST.get("content")
		category_id = request.POST.get("category")
		tag_ids = request.POST.getlist("tags")
		category = Category.objects.filter(id=category_id).first() if category_id else None
		blog = Blog.objects.create(title=title, author=author, content=content, category=category)
		if tag_ids:
			blog.tags.set(Tag.objects.filter(id__in=tag_ids))
		return redirect("/blog/")
	return render(request, "blog/add_blog.html", {"categories": categories, "tags": tags, "user": request.user})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def blog_edit(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	# 权限校验：仅作者或admin可编辑
	if not (request.user.is_authenticated and (request.user == blog.user or request.user.is_superuser or request.user.username == blog.author)):
		return HttpResponse('无权编辑此博客', status=403)
	categories = Category.objects.all()
	tags = Tag.objects.all()
	if request.method == "POST":
		blog.title = request.POST.get("title")
		# 强制使用当前登录用户名
		blog.author = request.user.username if request.user.is_authenticated else "匿名"
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
	return render(request, "blog/edit_blog.html", {"blog": blog, "categories": categories, "tags": tags, "user": request.user})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def blog_delete(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	# 权限校验：仅作者或admin可删除
	if not (request.user.is_authenticated and (request.user == blog.user or request.user.is_superuser)):
		return HttpResponse('无权删除此博客', status=403)
	if request.method == "POST":
		blog.delete()
		return redirect("/blog/")
	return render(request, "blog/delete_blog.html", {"blog": blog})
