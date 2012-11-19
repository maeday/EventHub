import base64, cgi, datetime, hashlib, hmac, json, random, urllib

from EventHub import settings

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from accounts.forms import EmailAuthenticationForm, EmailUserCreationForm, \
    ForgotPasswordForm, ResetPasswordForm, isUniqueEmail, isUniqueFbid
from accounts.models import UserProfile, FacebookSession, User

###############################################################################
# Facebook signed request parser taken from:
# http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    b64str = unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/')))
    return base64.b64decode(b64str)

def parse_signed_request(signed_request, secret):
    '''Parse signed request returned from Facebook registration API'''
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        #log.error('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, 
                                digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        #log.debug('valid signed request received..')
        return data

# end code snippet
###############################################################################

@csrf_exempt
@never_cache
def register(request):
    '''Handle user registration request'''
    template = 'accounts/register-1.html'
    template_context = {
        'app_id': settings.FACEBOOK_APP_ID,
        'web_root': settings.WEB_ROOT
    }
    if request.user.is_authenticated():
        # They are already logged on, don't let them register again
        return redirect('/mypage')
    if request.POST:
        template = 'accounts/register-2.html'
        template_context['post_request'] = True
        
        if request.POST.get('signed_request'):
            # Post request received from first page (through Facebook API)
            signed_request = request.POST.get('signed_request')
            data = parse_signed_request(signed_request, settings.FACEBOOK_APP_SECRET)
            register_info = data['registration']
            if 'name' in register_info:
                name_parts = register_info['name'].split(u' ')
                template_context['firstname'] = name_parts[0]
                template_context['lastname'] = name_parts[len(name_parts)-1]
            else:
                template_context['firstname'] = register_info['first_name']
                template_context['lastname'] = register_info['last_name']
            template_context['email'] = register_info['email']
            
            valid = True
            if not isUniqueEmail(template_context['email']):
                valid = False
                template_context['used_email'] = True
                
            template_context['fbid'] = -1
            if 'user_id' in data:
                template_context['has_fbid'] = True
                template_context['redir_uri'] = settings.WEB_ROOT + '/connect'
                template_context['fbid'] = data['user_id']
                if not isUniqueFbid(template_context['fbid']):
                    valid = False
                    template_context['used_fbid'] = True
            
            if not valid:
                template = 'accounts/register-1.html'
        else:
            # Post request received from second page
            form = EmailUserCreationForm(request.POST) # A form bound to the POST data
            if form.is_valid(): 
                # All validation rules pass
                template_context['extra'] = 'SUCCESS'
                
                # Create new user
                new_user = form.save(request.POST.copy())
                
                # Build activation key
                username = new_user.username
                salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt+username).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                
                # Create and save user and profile
                new_profile = new_user.get_profile()
                new_profile.activation_key = activation_key
                new_profile.key_expires = key_expires
                new_profile.save()
    
                # Send an email with the confirmation link (disabled for now)
                email = new_user.email                                                                                                                    
                email_subject = 'Your new EventHub account confirmation'
                email_template = get_template('accounts/email/register.txt')
                context = Context({
                    'email'          : email,
                    'web_root'       : settings.WEB_ROOT,
                    'activation_key' : activation_key
                })
                email_body = email_template.render(context)
                send_mail(email_subject,
                          email_body,
                          'accounts-noreply@theeventhub.com',
                          [email])
                
                # Redirect to 'My Page' after successful registration
                return redirect('/login?register=success')
            else:
                template_context['extra'] = form.errors
        
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def confirm(request, activation_key):
    '''Confirm user's activation key'''
    template = 'accounts/confirm.html'
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
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def user_login(request):
    '''Allow user to log in'''
    template = 'accounts/login.html'
    template_context = {
        'logged_in' : False,
        'success'   : False,
        'active'    : True,
        'invalid'   : False,
        'app_id'    : settings.FACEBOOK_APP_ID,
        'redir_uri' : settings.WEB_ROOT + '/loginfb'
    }
    if request.user.is_authenticated():
        # User is already logged in; redirect to 'My Page'
        return redirect('/mypage')
    else:
        if request.POST:
            form = EmailAuthenticationForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('/mypage')
            else:
                # Username/password combo incorrect
#                template_context['extra'] = form.errors
                template_context['form'] = form
                template_context['problem'] = form.non_field_errors
                template_context['invalid'] = True
        elif request.GET:
            if 'register' in request.GET:
                template_context['register'] = request.GET['register']
            elif 'error' in request.GET:
                template_context['error'] = request.GET['error']
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def user_logout(request):
    '''Allow user to log out'''
    # TODO: handle more cases (user not logged in, logout unsuccessful, etc.)
    logout(request)
    return redirect('/index', permanent=True)
    
def login_facebook(request):
    '''Allow user to log in through Facebook'''
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/mypage')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.WEB_ROOT + '/loginfb',
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'code': request.GET['code'],
            }
            
            #csrf_token = request.GET['state']

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            
            if not response:
                # TODO: Handle this in template
                error = 'AUTH_ERROR'
            
            else:
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
                        return HttpResponseRedirect('/mypage')
                    else:
                        error = 'AUTH_DISABLED'
                else:
                    error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    return redirect('/login?error='+error, permanent=True)
    #return render_to_response('accounts/login.html', template_context, context_instance=RequestContext(request))

@csrf_exempt
def connect(request):
    template = 'accounts/fbconnect.html'
    template_context = {
        'app_id': settings.FACEBOOK_APP_ID,
        'web_root': settings.WEB_ROOT
    }
    if request.user.is_authenticated():
        if request.user.get_profile().fbid != -1:
            # They already have an account connected, shouldn't be here
            return redirect('/mypage')
#        elif request.POST.get('signed_request'):
#            # Post request received from first page (through Facebook API)
#            signed_request = request.POST.get('signed_request')
#            data = parse_signed_request(signed_request, settings.FACEBOOK_APP_SECRET)
#            register_info = data['registration']
#            
#            # TODO: Should we check if email matches registered account?
#            
#            if 'user_id' in data:
#                template_context['has_fbid'] = True
#                template_context['redir_uri'] = settings.WEB_ROOT + '/connect'
#                template_context['fbid'] = data['user_id']
#                if not isUniqueFbid(template_context['fbid']):
#                    template_context['used_fbid'] = True
#                else:
#                    user = request.user
#                    profile = user.get_profile()
#                    profile.fbid = template_context['fbid']
#                    profile.save()
#                    template_context['success'] = True
#            else:
#                template_context['no_fbid'] = True
#        request_context = RequestContext(request, template_context)
#        return render_to_response(template, request_context)
    
        if request.GET:
            if 'code' in request.GET:
                args = {
                    'client_id': settings.FACEBOOK_APP_ID,
                    'redirect_uri': settings.WEB_ROOT + '/mypage',
                    'client_secret': settings.FACEBOOK_APP_SECRET,
                    'code': request.GET['code'],
                }
                
                #csrf_token = request.GET['state']
    
                url = 'https://graph.facebook.com/oauth/access_token?' + \
                        urllib.urlencode(args)
                response = cgi.parse_qs(urllib.urlopen(url).read())
                
                if not response:
                    # TODO: Handle this in template
                    error = 'AUTH_ERROR_EXPIRED'
                
                else:
                    access_token = response['access_token'][0]
                    expires = response['expires'][0]
        
                    facebook_session = FacebookSession.objects.get_or_create(
                        access_token=access_token,
                    )[0]
        
                    facebook_session.expires = expires
                    facebook_session.save()
                    
                    profile = facebook_session.query('me')
                    fbid = profile['id']
                    if (isUniqueFbid(fbid)):
                        user = request.user
                        profile = user.get_profile()
                        profile.fbid = fbid
                        profile.save()
                        error = 'SUCCESS'
                    else:
                        error = 'ALREADY_EXISTS'
                    
                    
        
#                    user = authenticate(token=access_token)
#                    if user:
#                        if user.is_active:
#                            login(request, user)
#                            return HttpResponseRedirect('/mypage')
#                        else:
#                            error = 'AUTH_DISABLED'
#                    else:
#                        error = 'AUTH_FAILED'
            elif 'error_reason' in request.GET:
                error = 'AUTH_DENIED'
    
        template_context = {'settings': settings, 'error': error}
        return redirect('/mypage?error='+error, permanent=True)
    else:
        return redirect('/login')
    
def dashboard(request):
    template = 'mypage.html'
    template_context = {
        'success'   : False,
        'active'    : True,
        'invalid'   : False,
        'app_id'    : settings.FACEBOOK_APP_ID,
        'redir_uri' : settings.WEB_ROOT + '/mypage'
    }
    
    if not request.user.is_authenticated():
        return redirect('/login')
    if request.GET:
        if 'code' in request.GET:
            return connect(request)
        elif 'error' in request.GET:
            template_context['error'] = request.GET['error']
            
    
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def forgot_password(request):
    template = 'accounts/forgot.html'
    template_context = {}
    success = False
    
    if request.user.is_authenticated():
        # User is already logged in. Should we let them reset it?
        return redirect('/index')
    
    if request.POST:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            # Email exists, send email to user
            success = True
            # Build activation key
            user = form.get_user()
            username = user.username
            salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Create and save user and profile
            new_profile = user.get_profile()
            new_profile.activation_key = activation_key
            new_profile.key_expires = key_expires
            new_profile.save()
    
            # Send an email with the confirmation link
            email = user.email                                                                                                                    
            email_subject = 'Resetting your EventHub account password'
            email_template = get_template('accounts/email/reset.txt')
            context = Context({
                'email'    : email,
                'web_root' : settings.WEB_ROOT,
                'key'      : activation_key
            })
            email_body = email_template.render(context)
            send_mail(email_subject,
                      email_body,
                      'accounts-noreply@theeventhub.com',
                      [email])
            
        template_context = {
            'form' : form,
            'success' : success
        }
            
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def reset_password(request, key):
    '''Confirm user's activation key'''
    template = 'accounts/resetpassword.html'
    template_context = {'key': key,
                        'success': False}
    # Trigger 404 if reset key is not valid
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=key)
    if user_profile.key_expires < timezone.now():
        # User's reset password key has expired
        template_context['expired'] = True
    else:
        if request.POST:
            # User sent request to reset password
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                # Passwords matched, change user's password
                new_password = form.cleaned_data['password1']
                user = user_profile.user
                user.set_password(new_password)
                user.save()
                
                # Set key to expired state so user cannot use same link to 
                # resetpassword
                user_profile.key_expires = timezone.now()
                template_context['success'] = True
            template_context['form'] = form
            
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def resend_key(request):
    template = 'accounts/resend.html'
    template_context = {}
    success = False
    
    if request.user.is_authenticated():
        # User is already logged in. Shouldn't be here
        return redirect('/index')
    
    if request.POST:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            # Email exists, send email to user
            success = True
            
            # Build activation key
            user = form.get_user()
            username = user.username
            salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Modify and save user profile
            profile = user.get_profile()
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.save()
            
            email = user.email                                                                                                                    
            email_subject = 'Your EventHub activation link'
            email_template = get_template('accounts/email/register.txt')
            context = Context({
                'email'          : email,
                'web_root'       : settings.WEB_ROOT,
                'activation_key' : activation_key
            })
            email_body = email_template.render(context)
            send_mail(email_subject,
                      email_body,
                      'accounts-noreply@theeventhub.com',
                      [email])
            
        template_context = {
            'form' : form,
            'success' : success
        }
            
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@csrf_exempt 
def edit_profile(request):
    if request.POST:
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        userEmail = request.POST.get('userEmail')
        useFbPic = request.POST.get('useFbPic')
        userPic = request.FILES.get('userPic')
        user = authenticate(email=userEmail, password=oldPassword)
        template_context = {'text': "1"}
        if user is not None:
            if user.is_active:
            		user.first_name=firstName
            		user.last_name=lastName
            		if len(newPassword)>0:
            		    user.set_password(newPassword)
            		userProfile = user.get_profile()
            		if useFbPic=='1':
            		    userProfile.use_fb_pic=True
            		else:
            		    userProfile.use_fb_pic=False
            		    userProfile.pic = userPic
            		userProfile.save()
            		user.save()
                #login(request, user)
            else:
                template_context = {'text': "3"}
                #state = "Your account is not active."
        else:
            template_context = {'text': "2"}
            #state = "Your username and/or password were incorrect."

        template = 'text.html'
        request_context = RequestContext(request, template_context)
        return render_to_response(template, request_context)
    
