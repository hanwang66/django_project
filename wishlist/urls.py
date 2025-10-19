from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_list, name='wishlist_list'),
    path('add/', views.wishlist_add, name='wishlist_add'),
    path('<int:pk>/', views.wishlist_detail, name='wishlist_detail'),
    path('<int:pk>/edit/', views.wishlist_edit, name='wishlist_edit'),
    path('<int:pk>/delete/', views.wishlist_delete, name='wishlist_delete'),
    path('<int:wishlist_id>/add_item/', views.wishlistitem_add, name='wishlistitem_add'),
    path('<int:wishlist_id>/item/<int:item_id>/edit/', views.wishlistitem_edit, name='wishlistitem_edit'),
    path('<int:wishlist_id>/item/<int:item_id>/delete/', views.wishlistitem_delete, name='wishlistitem_delete'),
    path('<int:wishlist_id>/item/<int:item_id>/done/', views.wishlistitem_done, name='wishlistitem_done'),
    path('<int:wishlist_id>/item/<int:item_id>/undone/', views.wishlistitem_undone, name='wishlistitem_undone'),
]
