"""
URL configuration for iproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render

def index(request):
    from blog.models import Blog
    from real_estate.models import RealEstate
    from stock.models import Stock
    blog_count = Blog.objects.count()
    realestate_count = RealEstate.objects.count()
    stock_count = Stock.objects.count()
    return render(request, "index.html", {
        "blog_count": blog_count,
        "realestate_count": realestate_count,
        "stock_count": stock_count,
    })

urlpatterns = [
    path('', index, name='index'),
    path("admin/", admin.site.urls),
    path("auth/", include("custom_auth.urls")),
    path("blog/", include("blog.urls")),
    # path("info/", include("info.urls")),  # 已删除信息录入功能
    path("stock/", include("stock.urls")),
    path("real_estate/", include("real_estate.urls")),
]
