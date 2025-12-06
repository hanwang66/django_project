from django.contrib import admin
from .models import OperationLog


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'method', 'path', 'ip_address', 'created_at')
    list_filter = ('action', 'method', 'created_at')
    search_fields = ('user__username', 'path', 'params')
    readonly_fields = ('user', 'action', 'path', 'method', 'ip_address', 'params', 'created_at')
    
    # 禁止在后台手动添加或修改日志，保证审计数据的真实性
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
