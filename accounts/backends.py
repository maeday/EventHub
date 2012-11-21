# from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from accounts import models

###############################################################################
# Following code taken and modified from 
# https://bitbucket.org/tino/django-email-login

class EmailBackend(ModelBackend):
    
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email__iexact=email.lower())
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

# end code snippet
###############################################################################

class FacebookBackend:
    
    def authenticate(self, token=None):

        facebook_session = models.FacebookSession.objects.get(
            access_token=token,
        )

        profile = facebook_session.query('me')
   
        try:
            # Try to get user from DB
            profile = models.UserProfile.objects.get(fbid=profile['id'])
            #user = User.objects.get(username=profile['id'])
            user = profile.user
        except models.UserProfile.DoesNotExist:
            # User does not exist, so create a new user
            #user = User(username=profile['id'])
            return None
    
#        # Update user info (is this necessary?)
#        user.set_unusable_password()
#        user.email = profile['email']
#        user.first_name = profile['first_name']
#        user.last_name = profile['last_name']
#        user.save()
#
#        try:
#            models.FacebookSession.objects.get(uid=profile['id']).delete()
#        except models.FacebookSession.DoesNotExist, e:
#            pass
#
#        facebook_session.uid = profile['id']
#        facebook_session.user = user
#        facebook_session.save()
   
        return user
   
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None