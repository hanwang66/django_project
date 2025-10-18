from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('add/', views.blog_add, name='blog_add'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]
