from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from config.settings import DEBUG


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not DEBUG:
        if created:
            from .tasks import create_profile
            create_profile.delay(instance.id)
    else:
        if created:
            Profile.objects.create(user=instance)
