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

from django.db.models import Q

def index(request):
     latest_event_list = Event.objects.all().order_by('start_date').exclude(
                         end_date__lt=datetime.now())
     categories_list = Categories.objects.all()
     neighborhoods_list = Neighborhoods.objects.all()     
     
     template = 'index.html'
     template_context = {'latest_event_list': latest_event_list,
                         'categories_list': categories_list,
                         'neighborhoods_list': neighborhoods_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)
     
def eventlist(request):
     latest_event_list = Event.objects.all().order_by('start_date').exclude(
                         end_date__lt=datetime.now())
     
     template = 'eventlist.html'
     template_context = {'latest_event_list': latest_event_list}
     request_context = RequestContext(request, template_context)
     
     return render_to_response(template, request_context)
  
@csrf_exempt   
def filterlist(request):
    #month = request.POST.get('month')
    #day = request.POST.get('day')
    #year = request.POST.get('year')
    #date = month+' '+day+' '+year
    neighborhoods = request.POST.get('locations')
    categories = request.POST.get('categories')
    keywords = request.POST.get('keywords')
    neighborhoods_array = neighborhoods.split(',')
    categories_array = categories.split(',')
    keywords_array = keywords.split(',')
    event_list = Event.objects.all()
    #if date!=null:
    #     date_field = datetime.strptime(date, '%b %d %Y') 
    #	event_list = event_list.filter(start_date__lte=date_field,
    #end_date__gte=date_field)
    if neighborhoods:
        q = Q(neighborhood__id__exact=neighborhoods_array[0]) 
        for neighborhood in neighborhoods_array[1:]:
            q.add(Q(neighborhood__id__exact=neighborhood),Q.OR)
        event_list = event_list.filter(q)
    if categories:
        q = Q(categories__id__exact=categories_array[0]) 
        for category in categories_array[1:]:
            q.add(Q(categories__id__exact=category),Q.OR)
        event_list = event_list.filter(q).distinct()
    if keywords:
        q = Q(name__icontains=keywords_array[0]) 
        for keyword in keywords_array:
            q.add(Q(name__icontains=keyword),Q.OR)
        event_list = event_list.filter(q).distinct()
    
    event_list = event_list.order_by('start_date').exclude(
                 end_date__lt=datetime.now())
        
    template = 'eventlist.html'
    template_context = {'latest_event_list': event_list}
    request_context = RequestContext(request, template_context)
    
    return render_to_response(template, request_context)

def event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    template = 'event.html'
    address = "%s, %s, %s %s" % (event.street, event.city, event.state, event.zipcode)
    template_context = {'event': event,
                        'address': address}
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@csrf_exempt
def create_event(request):
     if request.user.is_authenticated():
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
              eMinCost = request.POST.get('cost-min')
              eMaxCost = request.POST.get('cost-max')
              eNeighborhood = request.POST.get('location')
              eCategoriesString = request.POST.get('categories')
              eimage = request.FILES.get('image')
              
              startDateTime = datetime.strptime(eStartDateTimeString, "%m/%d/%Y %I:%M %p")
              endDateTime = datetime.strptime(eEndDateTimeString, "%m/%d/%Y %I:%M %p")
              
              eCategories = eCategoriesString.split(',')
              
              u = request.user
              n = Neighborhoods(id=eNeighborhood)
              e = Event(start_date=startDateTime, end_date=endDateTime, name=eName, 
                        poster=u, description=eDesc, free=False, neighborhood=n,
                        cost_max=eMaxCost, cost_min=eMinCost, venue=eVenue, url=eUrl,
                        street=eStreet, city=eCity, state=eState, zipcode=eZipcode, image=eimage)
              
              e.save()
              
              if eCategories:
                  for categoryNum in eCategories:
                      category = Categories.objects.get(id=categoryNum)
                      e.categories.add(category)
              
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
