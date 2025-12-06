from django.urls import path
from . import views

app_name = 'english'

urlpatterns = [
    path('', views.submit_record, name='submit_record'),
    path('overview/', views.overview, name='overview'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('detail/<int:pk>/', views.record_detail, name='record_detail'),
]