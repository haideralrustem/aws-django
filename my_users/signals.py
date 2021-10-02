from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)   # <------ Event
def create_profile(sender, instance, created,  **kwargs):   # <--- receive signal and do something
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)   # <------ Send out signal when a user is saved!
def save_profile(sender, instance, created,  **kwargs):   # <--- receiver signal and do something
    instance.profile.save()   # save the profile

