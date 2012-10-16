from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from events.models import Event

def index(request):
     latest_event_list = Event.objects.all().order_by('-upload_date')[:5]
     
     template = 'events/index.html'
     template_context = {'latest_event_list': latest_event_list}
     
     return render_to_response(template, template_context)

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
          template = 'events/change_event_name.html'
          
          return render_to_response(template)
