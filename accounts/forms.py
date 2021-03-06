from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

import base64
import hashlib

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

import re
from accounts.models import UserProfile

alnum_re = re.compile(r'^\w+$')

from django.utils.functional import lazy

lazy_inter = lazy(lambda a,b: str(a) % b, str)

# Validation error messages
ERROR_MSG_INCORRECT_USERPASS = \
    'Please enter a correct email address and password.'
ERROR_MSG_USER_INACTIVE = \
    'This account is inactive. Please check your email for the activation link. If you have lost it, or it has expired, please go <a href="/resend">here</a> to get a new link sent to your email.'

def isUniqueEmail(field_data):
    '''Test if email is unique'''
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return True
    return False

def isUniqueFbid(fbid):
    '''Test if Facebook ID is unique'''
    if (fbid != -1):
        try:
            UserProfile.objects.get(fbid=fbid)
        except UserProfile.DoesNotExist:
            return True
    return False

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
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The email "%s" has already been used.' 
                                     % field_data)

def isAlphaNumeric(field_data):
    '''Checks to make sure the field is alpha-numeric'''
    if not alnum_re.search(field_data):
        raise validators.ValidationError("This value must contain only letters, \
        numbers and underscores.")

    
###############################################################################
# Following code taken and modified from 
# https://bitbucket.org/tino/django-email-login

def email_to_username(email):
    return base64.urlsafe_b64encode(hashlib.sha256(email.lower()).digest())[:30]

class EmailAuthenticationForm(forms.Form):
    """
    Form for authenticating users by their email address.
    """
    email = forms.EmailField(label="Email address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

#    def __init__(self, request=None, *args, **kwargs):
#        """
#        If request is passed in, the form will validate that cookies are
#        enabled. Note that the request (a HttpRequest object) must have set a
#        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
#        running this validation.
#        """
#        self.request = request
#        self.user_cache = None
#        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('email') :
            raise forms.ValidationError(_("Please enter a valid email address."))
        
        email = self.cleaned_data.get('email').lower()
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_(ERROR_MSG_INCORRECT_USERPASS))
            elif not self.user_cache.is_active:
                # User hasn't been activated; allow login for now
                #pass
                raise forms.ValidationError(mark_safe(ERROR_MSG_USER_INACTIVE))
#        self.check_for_test_cookie()
        return self.cleaned_data

#    def check_for_test_cookie(self):
#        if self.request and not self.request.session.test_cookie_worked():
#            raise forms.ValidationError(
#                _("Your Web browser doesn't appear to have cookies enabled. "
#                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class EmailUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email
    address and password.
    """
    email = forms.EmailField(label = "Email address")
    password1 = forms.CharField(
        label  = "Password", 
        widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label     = "Password confirmation", 
        widget    = forms.PasswordInput,
        help_text = "Enter the same password as above, for verification."
    )
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")
    fbid = forms.IntegerField(label = "Facebook ID")

    class Meta:
        model = User
        fields = ("email",)
        
    def clean_email(self):
        """ Validates that the email address is not already in use. """
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("A user with that email address already exists."))
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def clean_fbid(self):
        fbid = self.cleaned_data["fbid"]
        if fbid != -1:
            try:
                UserProfile.objects.get(fbid=fbid)
            except UserProfile.DoesNotExist:
                return fbid
            raise forms.ValidationError(_("A user with that Facebook account already exists."))
        return fbid
        
    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.username = email_to_username(user.email)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = False
        if commit:
            user.save()
            profile = user.get_profile()
            profile.fbid = self.cleaned_data["fbid"]
            profile.save()
        return user

class EmailUserChangeForm(forms.ModelForm):
    email = forms.EmailField(label=_("Email address"))

    class Meta:
        model = User
        exclude = ('username',)

    def __init__(self, *args, **kwargs):
        super(EmailUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
            
    def save(self, commit=True):
        user = super(EmailUserChangeForm, self).save(commit=False)
        user.username = email_to_username(user.email)
        if commit:
            user.save()
        return user

# end code snippet
###############################################################################

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email address")
    
    def clean_email(self):
        """ Validates that the email address exists in the database."""
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email__iexact=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError(_("No user exists with that email address."))
        
    def get_user(self):
        email = self.cleaned_data["email"].lower()
        return User.objects.get(email__iexact=email)

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="New Password (again)", widget=forms.PasswordInput)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2