from django.shortcuts import render, get_object_or_404, redirect
from .models import Info
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def info_index(request):
	infos = Info.objects.all().order_by('-created_at')
	return render(request, "info/list_info.html", {"infos": infos})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def info_detail(request, pk):
	info = get_object_or_404(Info, pk=pk)
	return render(request, "info/detail_info.html", {"info": info})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def info_add(request):
	if request.method == "POST":
		name = request.POST.get("name")
		email = request.POST.get("email")
		message = request.POST.get("message")
		Info.objects.create(name=name, email=email, message=message)
		return redirect("/info/")
	return render(request, "info/add_info.html")

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def info_edit(request, pk):
	info = get_object_or_404(Info, pk=pk)
	if request.method == "POST":
		info.name = request.POST.get("name")
		info.email = request.POST.get("email")
		info.message = request.POST.get("message")
		info.save()
		return redirect(f"/info/{pk}/")
	return render(request, "info/edit_info.html", {"info": info})

@user_passes_test(is_admin, login_url='/auth/login/', redirect_field_name=None)
def info_delete(request, pk):
	info = get_object_or_404(Info, pk=pk)
	if request.method == "POST":
		info.delete()
		return redirect("/info/")
	return render(request, "info/delete_info.html", {"info": info})
