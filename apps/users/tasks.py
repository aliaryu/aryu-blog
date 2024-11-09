from config.settings import DEBUG

# i know this is not best practice, but its just is an example ^^

if not DEBUG:
    from celery import shared_task
    from .models import Profile

    @shared_task
    def create_profile(user_id):
        Profile.objects.create(user_id=user_id)
