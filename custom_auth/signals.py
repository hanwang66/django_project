from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 如果用户没有profile则自动创建
    try:
        profile = instance.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=instance)
    profile.save()
