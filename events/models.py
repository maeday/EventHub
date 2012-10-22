from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name=models.CharField(max_length=255)
    url=models.URLField()

class Cost(models.Model):
    cost=models.FloatField()

class Categories(models.Model):
    name=models.CharField(max_length=255)

class Event(models.Model):
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    poster = models.ForeignKey(User)
    post_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField() 
    location = models.ForeignKey(Location)
    cost = models.ManyToManyField(Cost)
    categories = models.ManyToManyField(Categories)
    # need PIL installed for image fields to work
    #image = models.ImageField()

    def __unicode__(self):
      return self.event_name



