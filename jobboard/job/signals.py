from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # создаст профиль если его нет; если уже есть — просто вернёт существующий
    Profile.objects.get_or_create(user=instance)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # создаём профиль только если его нет
    Profile.objects.get_or_create(user=instance)