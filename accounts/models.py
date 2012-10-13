import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    '''Class to store additional user information'''
    # Feel free to add any other fields we need
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, key_expires = datetime.datetime.now())

# Automatically create UserProfile for User if it doesn't already exist
post_save.connect(create_user_profile, sender=User)