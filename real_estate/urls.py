from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .api_views import RealEstateViewSet

router = DefaultRouter()
router.register('real-estate', RealEstateViewSet)

urlpatterns = [
    path('', views.realestate_index, name='realestate_index'),
    path('add/', views.realestate_add, name='realestate_add'),
    path('<int:pk>/', views.realestate_detail, name='realestate_detail'),
    path('<int:pk>/edit/', views.realestate_edit, name='realestate_edit'),
    path('<int:pk>/delete/', views.realestate_delete, name='realestate_delete'),
    path('trend_data/', views.realestate_trend_data, name='realestate_trend_data'),
    path('trend_list/', views.realestate_trend_list, name='realestate_trend_list'),
    path('api/', include(router.urls)),
]
