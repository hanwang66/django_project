from django.contrib import admin
from .models import RealEstate


@admin.register(RealEstate)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('community', 'area', 'city', 'floor', 'price', 'date')
	list_filter = ('community', 'area', 'city', 'floor', 'price', 'date')
	search_fields = ('community', 'area', 'city', 'floor', 'price', 'date')
