try: import simplejson as json
except ImportError: import json

from EventHub import settings

from accounts.views import connect

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from events.models import Event, Categories, Neighborhoods

def dashboard(request):
    template = 'mypage.html'

    categories_list = Categories.objects.all()
    neighborhoods_list = Neighborhoods.objects.all()     

    template_context = {
        'success'   : False,
        'active'    : True,
        'invalid'   : False,
        'app_id'    : settings.FACEBOOK_APP_ID,
        'redir_uri' : settings.WEB_ROOT + '/mypage',
        'categories_list': categories_list,
        'neighborhoods_list': neighborhoods_list
    }
    
    if not request.user.is_authenticated():
        return redirect('/login')
    if request.GET:
        if 'code' in request.GET:
            return connect(request)
        elif 'error' in request.GET:
            template_context['error'] = request.GET['error']
            
    template_context['user_events'] = request.user.events_posted.all().order_by('start_date')
    template_context['subscribed_events'] = request.user.events_following.all().order_by('start_date')
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

def profile(request, user_id):
    template = 'profile.html'
    template_context = {
        'app_id'    : settings.FACEBOOK_APP_ID,
        'redir_uri' : settings.WEB_ROOT + '/mypage',
    }
    
#    if not request.user.is_authenticated():
#        msg = "You must be logged in to view other user's profiles."
#        messages.add_message(request, messages.ERROR, msg)
#        return redirect('/login?next=/profile/'+user_id)

    user = get_object_or_404(User, id=user_id)
    template_context['p_user'] = user
    template_context['user_events'] = user.events_posted.all().order_by('start_date')
    template_context['subscribed_events'] = user.events_following.all().order_by('start_date')
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)