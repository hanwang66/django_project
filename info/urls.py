from django.urls import path
from . import views

urlpatterns = [
path('', views.info_index, name='info_index'),
path('add/', views.info_add, name='info_add'),
path('<int:pk>/', views.info_detail, name='info_detail'),
path('<int:pk>/edit/', views.info_edit, name='info_edit'),
path('<int:pk>/delete/', views.info_delete, name='info_delete'),
]
