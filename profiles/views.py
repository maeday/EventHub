from accounts.views import connect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext

from events.models import Event, Categories, Neighborhoods

@login_required
def dashboard(request):
    template = 'mypage.html'

    categories_list = Categories.objects.all()
    neighborhoods_list = Neighborhoods.objects.all()     

    template_context = {
        'success'   : False,
        'active'    : True,
        'invalid'   : False,
        'categories_list': categories_list,
        'neighborhoods_list': neighborhoods_list
    }
    
    if request.GET:
        if 'code' in request.GET:
            return connect(request)
        elif 'error' in request.GET:
            template_context['error'] = request.GET['error']
    
    user = request.user
    template_context['user_events'] = \
        user.events_posted.order_by('start_date')
    template_context['subscribed_events'] = \
        user.events_following.order_by('start_date')
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@login_required
def dashboard_unfollow(request, event_id):
    if request.user.is_authenticated():
        event_id = int(event_id)
        try:
            event = Event.objects.get(id=event_id)
            event.remove_follower(request.user)
            event.save()
            info_msg = 'You have unfollowed the event "' + event.name + '".'
            messages.add_message(request, messages.INFO, info_msg)
        except Event.DoesNotExist:
            error_msg = 'That event does not exist! It has either been deleted \
                or was never created.'
            messages.add_message(request, messages.ERROR, error_msg)
    return redirect('/mypage')

def profile(request, user_id):
    template = 'profile.html'
    template_context = {}
    user = get_object_or_404(User, id=user_id)
    template_context['p_user'] = user
    template_context['user_events'] = user.events_posted.all().order_by('start_date')
    template_context['subscribed_events'] = user.events_following.all().order_by('start_date')
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)