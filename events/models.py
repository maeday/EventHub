from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name=models.CharField(max_length=255)

# Create your models here.
class Event(models.Model):
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    poster = models.ForeignKey(User)
    post_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField() 
    cost_max = models.FloatField()
    cost_min = models.FloatField()
    #categories = models.ManyToManyField(Categories)
    location=models.CharField(max_length=255)
    url=models.URLField()
    # need PIL installed for image fields to work
    #image = models.ImageField()

    def __unicode__(self):
      return self.name



