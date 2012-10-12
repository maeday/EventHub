from django.db import models

# Create your models here.
class Event(models.Model):
  start_date = models.DateTimeField() 
	end_date = models.DateTimeField()
	event_name = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	upload_date = models.DateTimeField()
	lmodified = models.DateTimeField()
	description =models.TextField() 
	event_id = models.IntegerField(primary_key=True)
	location = models.CharField(max_length=255)
	cost = models.FloatField()
	categories = models.CharField(max_length=100)
	image = models.ImageField() 

class User(models.Model):
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	id = models.IntegerField(primary_key=True) 
	gender = models.CharField(max_length=1)
	email = models.EmailField() 