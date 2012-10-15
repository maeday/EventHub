from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from events.models import Event

def index(request):
     latest_event_list = Event.objects.all().order_by('-upload_date')[:5]
     return render_to_response('events/index.html', {'latest_event_list': latest_event_list})

def change_event_name(request, event_id):
     e = get_object_or_404(Event, id=event_id)
     new_name = request.POST['New Name for Event']
     e.event_name = new_name
     return HttpResponseRedirect(reverse('events.views.index'))
