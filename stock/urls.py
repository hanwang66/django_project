from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_index, name='stock_index'),
    path('add/', views.stock_add, name='stock_add'),
    path('<int:pk>/', views.stock_detail, name='stock_detail'),
    path('<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('<int:pk>/delete/', views.stock_delete, name='stock_delete'),
]
