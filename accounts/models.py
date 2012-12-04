import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

try: import simplejson as json
except ImportError: import json

class UserProfile(models.Model):
    '''Class to store additional user information'''
    # Feel free to add any other fields we need
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    fbid = models.BigIntegerField(default=-1)
	picUrl = models.URLField(max_length=255, null=True)
    pic = models.ImageField(upload_to="pics/", null=True)
    use_fb_pic = models.BooleanField(default=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance, 
                                   key_expires = datetime.datetime.now(), 
                                   fbid = -1)

# Automatically create UserProfile for User if it doesn't already exist
post_save.connect(create_user_profile, sender=User)

# Facebook Authentication code from http://djangosnippets.org/snippets/2065/
class FacebookSessionError(Exception):   
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self): 
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)
        
class FacebookSession(models.Model):

    access_token = models.CharField(max_length=300, unique=True)
    expires = models.IntegerField(null=True)
        
    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)
        
    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))
        
    def query(self, object_id, connection_type=None, metadata=False):
        import urllib
        
        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)
        
        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1
         
        url += '?' + urllib.urlencode(params)
        response = json.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response