from django.db import models
from django.conf import settings

class OperationLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', '新增'),
        ('UPDATE', '修改'),
        ('DELETE', '删除'),
        ('ACCESS', '访问/查询'), # 如果你想记录查询，可以保留这个，但数据量会很大
        ('OTHER', '其他'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="操作人"
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name="动作类型")
    path = models.CharField(max_length=255, verbose_name="请求路径")
    method = models.CharField(max_length=10, verbose_name="请求方法")
    ip_address = models.GenericIPAddressField(null=True, verbose_name="IP地址")
    # 使用 TextField 存储请求参数，生产环境建议用 JSONField (如果数据库支持)
    params = models.TextField(blank=True, null=True, verbose_name="请求参数") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.action} - {self.path}"
