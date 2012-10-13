from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()
    # renamed to 'name'?
    event_name = models.CharField(max_length=100)
    # renamed to 'poster'?
    user = models.ForeignKey(User)
    # renamed to 'post_date'?
    upload_date = models.DateTimeField()
    # renamed to 'last_modified'?
    lmodified = models.DateTimeField() 
    description = models.TextField() 
    # ID primary key is automatically created
#    event_id = models.IntegerField(primary_key=True)
    # should probably be relationship to Location object
    location = models.CharField(max_length=255)
    # what about events with varying costs?
    cost = models.FloatField()
    # not sure if this will actually work, should be a relationship
    categories = models.CharField(max_length=100)
    image = models.ImageField() 

# Django already has a User class
#class User(models.Model):
#    fname = models.CharField(max_length=50)
#    lname = models.CharField(max_length=50)
#    id = models.IntegerField(primary_key=True) 
#    gender = models.CharField(max_length=1)
#    email = models.EmailField() 