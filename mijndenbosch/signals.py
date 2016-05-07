from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Persoon

@receiver(post_save, sender=get_user_model())
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        try:
            p = Persoon.objects.get(email=user.email)
        except Persoon.DoesNotExist:
            p = Persoon(email=user.email, naam=user.username)
        if not p.user:
            p.user = user
            p.save()
