from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.utils import timezone

from EventHub import settings
from events.models import Event
from django.contrib.auth.models import User

def index(request):
     latest_event_list = Event.objects.all()
     
     template = 'index.html'
     template_context = {'latest_event_list': latest_event_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)
     
def eventlist(request):
     latest_event_list = Event.objects.all()
     
     template = 'eventlist.html'
     template_context = {'latest_event_list': latest_event_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)

@csrf_exempt
def create_event(request):
     if request.POST:
          eName = request.POST.get('title')
          eDesc = request.POST.get('description')
          
          u = User(id=1)
          e = Event(start_date=timezone.now(), end_date=timezone.now(), name=eName, 
                    poster=u, description=eDesc,
                    cost_max=10.0, cost_min=0.0, location="UW", url="www.uw.edu")
          e.save()
          
          template = 'text.html'
          template_context = {'text': "1"}
          request_context = RequestContext(request, template_context)
     
          return render_to_response(template, request_context)
     else:
          template = 'text.html'
          template_context = {}
          request_context = RequestContext(request, template_context)
     
          return render_to_response(template, request_context)

"""
@csrf_exempt
def change_event_name(request):     
     if request.POST:
          eid = request.POST.get('eventid')
          e = Event.objects.get(id=eid)
          new_name = request.POST.get('newname')
          e.event_name = new_name
          e.save()
          
          return HttpResponseRedirect(reverse('events.views.index'))
     else:
          return index(request)
"""
