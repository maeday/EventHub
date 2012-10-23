import datetime, hashlib, random

import cgi
import urllib

from EventHub import settings

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone

from accounts.forms import RegistrationForm, LoginForm
from accounts.models import UserProfile, FacebookSession

def register(request):
    '''Handle user registration request'''
    template = 'register.html'
    template_context = {}
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response(template, {'has_account': True})
    if request.POST:
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Get user input
            email = form._raw_value('email')
            username = form._raw_value('username')
            
            # Build activation key
            salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha224(salt+username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Create and save user and profile
            new_user = form.save(request.POST.copy())
            new_profile = new_user.get_profile()
            new_profile.activation_key = activation_key
            new_profile.key_expires = key_expires
            new_profile.save()

            # Send an email with the confirmation link                                                                                                                      
            email_subject = 'Your new example.com account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an \
eventhub.com account!\n\nTo activate your account, click this link within 48 \
hours:\n\nhttp://127.0.0.1:8000/register/confirm/%s" % (username, activation_key)
            send_mail(email_subject,
                      email_body,
                      'accounts-noreply@eventhub.com',
                      [email])
            template_context = {'created': True}
        else:
            # Form validation failed
            errors = form.errors
            template_context = {
                'form'    : form,
                'created' : False,
                'invalid' : True,
                'errors'  : errors
            }
    else:
        # No registration request
        form = RegistrationForm
        template_context = {
            'created' : False,
            'form'    : form
        }
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

FACEBOOK_APP_ID = "BLAHBLAHBLAH"

def register2(request):
    '''Handle user registration request'''
    template = 'register2.html'
    template_context = {}
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response(template, {'has_account': True})
    if request.POST:
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Get user input
            email = form._raw_value('email')
            username = form._raw_value('username')
            
            # Build activation key
            salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha224(salt+username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Create and save user and profile
            new_user = form.save(request.POST.copy())
            new_profile = new_user.get_profile()
            new_profile.activation_key = activation_key
            new_profile.key_expires = key_expires
            new_profile.save()

            # Send an email with the confirmation link                                                                                                                      
            email_subject = 'Your new example.com account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an \
eventhub.com account!\n\nTo activate your account, click this link within 48 \
hours:\n\nhttp://127.0.0.1:8000/register/confirm/%s" % (username, activation_key)
            send_mail(email_subject,
                      email_body,
                      'accounts-noreply@eventhub.com',
                      [email])
            template_context = {'created': True}
        else:
            # Form validation failed
            errors = form.errors
            template_context = {
                'form'    : form,
                'created' : False,
                'invalid' : True,
                'errors'  : errors
            }
    else:
        # No registration request
        form = RegistrationForm
        template_context = {
            'created' : False,
            'form'    : form
        }
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def confirm(request, activation_key):
    '''Confirm user's activation key'''
    template = 'confirm.html'
    template_context = {}
    if request.user.is_authenticated():
        # User is already logged on and activated
        template_context = {'has_account': True}
    else:
        # Trigger 404 if activation key is not valid
        user_profile = get_object_or_404(UserProfile,
                                         activation_key=activation_key)
        if user_profile.key_expires < timezone.now():
            # User's activation key has expired
            template_context = {'expired': True}
        else:
            # Activate user
            user_account = user_profile.user
            user_account.is_active = True
            user_account.save()
            template_context = {'success': True}
    return render_to_response(template, template_context)

def user_login(request):
    '''Allow user to log in'''
    template = 'login.html'
    template_context = {
        'logged_in' : False,
        'success'   : False,
        'active'    : True,
        'invalid'   : False,
        'form'      : LoginForm,
        'username'  : ''
    }
    if request.user.is_authenticated():
        # User is already logged in
        # TODO: Figure out how this should be handled
        template_context['logged_in'] = True
    else:
        if request.POST:
            # Login request sent
            username = request.POST.get('username')
            password = request.POST.get('password')
    
            template_context['username'] = username
            user = authenticate(username=username, password=password)
            if user is not None:
                # Unable to authenticate
                if user.is_active:
                    # User has been activated
                    login(request, user)
                    template_context['success'] = True
                else:
                    # User has not yet been activated
                    template_context['active'] = False
            else:
                # Username/password combo incorrect
                template_context['invalid'] = True
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def user_logout(request):
    '''Allow user to log out'''
    # TODO: handle more cases (user not logged in, logout unsuccessful, etc.)
    logout(request)
    form = LoginForm
    state = "You have successfully logged out!"
    return render_to_response('logout.html', 
                              RequestContext(request, 
                                             {'state': state, 'form': form}))
    
def login_facebook(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/yay/')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = authenticate(token=access_token)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/yay/')
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    return render_to_response('login.html', template_context, context_instance=RequestContext(request))
