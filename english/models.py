from django.db import models
from django.contrib.auth.models import User


class EnglishStudyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.TextField(max_length=100, default='未命名')
    content = models.TextField()
    duration = models.PositiveIntegerField(help_text="学习时长（分钟）")
    tips = models.TextField(blank=True, null=True, help_text="备注")

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.duration}min"

    class Meta:
        ordering = ['-date']
        verbose_name = "英语学习记录"
