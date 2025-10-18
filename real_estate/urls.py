from django.urls import path
from . import views

urlpatterns = [
    path('', views.realestate_index, name='realestate_index'),
    path('add/', views.realestate_add, name='realestate_add'),
    path('<int:pk>/', views.realestate_detail, name='realestate_detail'),
    path('<int:pk>/edit/', views.realestate_edit, name='realestate_edit'),
    path('<int:pk>/delete/', views.realestate_delete, name='realestate_delete'),
    path('trend_data/', views.realestate_trend_data, name='realestate_trend_data'),
    path('trend_list/', views.realestate_trend_list, name='realestate_trend_list'),
]
