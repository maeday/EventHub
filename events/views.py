from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.utils import timezone

from EventHub import settings
from events.models import Event, Categories, Neighborhoods
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField

from datetime import datetime

def index(request):
     latest_event_list = Event.objects.all().order_by('start_date')
     categories_list = Categories.objects.all()
     neighborhoods_list = Neighborhoods.objects.all()     
     
     template = 'index.html'
     template_context = {'latest_event_list': latest_event_list,
                         'categories_list': categories_list,
                         'neighborhoods_list': neighborhoods_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)
     
def eventlist(request):
     latest_event_list = Event.objects.all().order_by('start_date')
     
     template = 'eventlist.html'
     template_context = {'latest_event_list': latest_event_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)

def event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    template = 'event.html'
    template_context = {'event': event}
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@csrf_exempt
def create_event(request):
     if request.POST:
          eName = request.POST.get('title')
          eDesc = request.POST.get('description')
          eStartDateTimeString = request.POST.get('start')
          eEndDateTimeString = request.POST.get('end')
          eVenue = request.POST.get('venue')
          eStreet = request.POST.get('street')
          eCity = request.POST.get('city')
          eState = request.POST.get('state')
          eZipcode = request.POST.get('zip')
          eUrl = request.POST.get('url')
          eimage = request.FILES.get('image')
          
          startDateTime = datetime.strptime(eStartDateTimeString, "%m/%d/%Y %I:%M %p")
          endDateTime = datetime.strptime(eEndDateTimeString, "%m/%d/%Y %I:%M %p")
          
          u = User(id=1)
          n = Neighborhoods(id=1)
          e = Event(start_date=startDateTime, end_date=endDateTime, name=eName, 
                    poster=u, description=eDesc, free=False, neighborhood=n,
                    cost_max=10.0, cost_min=0.0, venue=eVenue, url=eUrl,
                    street=eStreet, city=eCity, state=eState, zipcode=eZipcode, image=eimage)
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

#def filter_events(request):
#	month = request.POST.get('month')
#	day = request.POST.get('day')
#	year = request.POST.get('year')
#	date = month+' '+day+' '+year
#	neighborhood = request.POST.get('neighborhood')
#	category = request.POST.get('category')
#	event_name = request.POST.get('search')
#	event_list = Event.objects.all()
#	if date!=null:
#		date_field = datetime.strptime(date, '%b %d %Y') 
#		event_list = event_list.filter(start_date__lte=date_field,
#	end_date__gte=date_field)
#	if neighborhood!=null:
#		event_list = event_list.filter(neighborhood__name__exact=neighborhood)
#	if category !=null:
#		event_list = event_list.filter(categories__name=category)
#	if search !=null:
#		event_list = event_list.filter(name__icontains=event_name)
#	
#	template = 'eventlist.html'
#	template_context = {'event_list': event_list}
#	request_context = RequestContext(request, template_context)
#     
#    return render_to_response(template, request_context)
