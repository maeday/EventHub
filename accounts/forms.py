from django import forms
from django.core import validators
from django.contrib.auth.models import User

import re

alnum_re = re.compile(r'^\w+$')

from django.utils.functional import lazy

lazy_inter = lazy(lambda a,b: str(a) % b, str)

def isValidUsername(field_data):
    '''Checks to make sure the username was given and it hasn't already been 
    taken'''
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The username "%s" is already taken.' 
                                     % field_data)

def isValidEmail(field_data):
    '''Checks to make sure the email was given and it hasn't already been 
    taken'''
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The email "%s" has already been used.' 
                                     % field_data)

def isAlphaNumeric(field_data):
    '''Checks to make sure the field is alpha-numeric'''
    if not alnum_re.search(field_data):
        raise validators.ValidationError("This value must contain only letters, \
        numbers and underscores.")
    
class RegistrationForm(forms.Form):
    '''Form used for user registration'''
#    username = forms.CharField(label='Username', max_length=30,
#                            required=True, validators=[isAlphaNumeric,
#                                                              isValidUsername])
    password = forms.CharField( widget=forms.PasswordInput, 
                                 max_length=60, label="Password")
    repassword = forms.CharField( widget=forms.PasswordInput, 
                                 max_length=60, label="Re-enter Password")
    # Django automatically checks to see if the email address is valid
    email = forms.EmailField( label='Email', max_length=30, required=True, validators=[isValidEmail] )
    fbid = forms.IntegerField( label='Facebook ID')
    
    # Verify that password2 matches password1
    def clean_password2(self):
        pw1 = self.cleaned_data['password']
        pw2 = self.cleaned_data['repassword']
        if pw1 != pw2:
            raise forms.ValidationError("The entered passwords do not match!")
        # Always return the cleaned data, whether you have changed it or not.
        return pw2
    
    def save(self, new_data):
        '''Creates a new user, saves it to the database, and returns it'''
        #u = User.objects.create_user(new_data['username'],
        # User email as username
        u = User.objects.create_user(new_data['email'],
                                     new_data['email'],
                                     new_data['password'])
        u.is_active = False
        u.save()
        return u
    
class LoginForm(forms.Form):
    '''Form used for user login'''
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField( widget=forms.PasswordInput, 
                                max_length=60, label="Password" )