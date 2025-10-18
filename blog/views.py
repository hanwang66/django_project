from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.http import HttpResponse

def blog_index(request):
	blogs = Blog.objects.all().order_by('-created_at')
	return render(request, "blog/list_blog.html", {"blogs": blogs})

def blog_detail(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	return render(request, "blog/blog_detail.html", {"blog": blog})

def blog_add(request):
	if request.method == "POST":
		title = request.POST.get("title")
		author = request.POST.get("author")
		content = request.POST.get("content")
		Blog.objects.create(title=title, author=author, content=content)
		return redirect("/blog/")
	return render(request, "blog/add_blog.html")

def blog_edit(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	if request.method == "POST":
		blog.title = request.POST.get("title")
		blog.author = request.POST.get("author")
		blog.content = request.POST.get("content")
		blog.save()
		return redirect(f"/blog/{pk}/")
	return render(request, "blog/edit_blog.html", {"blog": blog})

def blog_delete(request, pk):
	blog = get_object_or_404(Blog, pk=pk)
	if request.method == "POST":
		blog.delete()
		return redirect("/blog/")
	return render(request, "blog/delete_blog.html", {"blog": blog})
