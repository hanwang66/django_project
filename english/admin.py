from django.contrib import admin
from .models import EnglishStudyRecord

@admin.register(EnglishStudyRecord)
class EnglishStudyRecordAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'duration')
	list_filter = ('date', 'user')
	search_fields = ('user__username', 'content', 'tips')

# Register your models here.
