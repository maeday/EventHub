import datetime, hashlib, random

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone

from accounts.forms import RegistrationForm, LoginForm
from accounts.models import UserProfile

def register(request):
    '''Handle user registration request'''
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('register.html', {'has_account': True})
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
hours:\n\nhttp://127.0.0.1:8000/register/confirm/%s" % (
                username,
                activation_key)
            send_mail(email_subject,
                  email_body,
                  'accounts-noreply@eventhub.com',
                  [email])
            return render_to_response('register.html', 
                                      RequestContext(request, 
                                                     {'created': True}))
        else:
            errors = form.errors
            return render_to_response('register.html', 
                                      RequestContext(request, 
                                                     {'form': form, 
                                                      'created': False, 
                                                      'invalid': True, 
                                                      'errors': errors }))
    else:
        return render_to_response('register.html', 
                                      RequestContext(request, 
                                                     {'created': False, 
                                                      'invalid': True}))
    form = RegistrationForm
    return render_to_response('register.html', 
                              RequestContext(request, {'form': form}))

def confirm(request, activation_key):
    '''Confirm user's activation key'''
    if request.user.is_authenticated():
        return render_to_response('confirm.html', {'has_account': True})
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm.html', {'expired': True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success': True})

def login_user(request):
    '''Allow user to log in'''
    if request.user.is_authenticated():
        state = "You are already logged in!"
        return render_to_response('login.html', 
                                  {'already_logged_in': True, 
                                   'state': state})
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account has not yet been activated. \
                Please check your email for the activation link."
        else:
            state = "Your username and/or password were incorrect."

    form = LoginForm
    return render_to_response('login.html', 
                              RequestContext(request, 
                                             {'state': state, 
                                              'username': username, 
                                              'form': form}))

def logout_user(request):
    '''Allow user to log out'''
    # TODO: handle more cases (user not logged in, logout unsuccessful, etc.)
    logout(request)
    form = LoginForm
    state = "You have successfully logged out!"
    return render_to_response('logout.html', 
                              RequestContext(request, 
                                             {'state': state, 'form': form}))