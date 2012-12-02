from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name=models.CharField(max_length=255)
    
    def __unicode__(self):
      return self.name
    
class Neighborhoods(models.Model):
    name=models.CharField(max_length=255)
	
    def __unicode__(self):
      return self.name

# Create your models here.
class Event(models.Model):
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    poster = models.ForeignKey(User, related_name='events_posted')
    post_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField() 
    cost_max = models.FloatField()
    cost_min = models.FloatField()
    free = models.BooleanField()
    categories = models.ManyToManyField(Categories)
    neighborhood=models.ForeignKey(Neighborhoods)
    street = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=30, default='')
    zipcode = models.CharField(max_length=10, default='')
    image_url = models.CharField(max_length=255, null=True)
    venue = models.CharField(max_length=100, default='')
    url=models.URLField()
    # need PIL installed for image fields to work
    image = models.ImageField(upload_to="images/", null=True)
    followers = models.ManyToManyField(User, related_name='events_following')

    def __unicode__(self):
        return self.name
    
    def add_follower(self, user):
        self.followers.add(user)
    
    def remove_follower(self, user):
        self.followers.remove(user)
        
    def user_is_follower(self, user):
        return user in self.followers.all()



