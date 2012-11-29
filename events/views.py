import random

from django.core.cache import cache

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

from django.db import IntegrityError

from django.db.models import Q
from django.db.models.query import QuerySet

# Code from http://jeffelmore.org/2010/09/25/smarter-caching-of-django-querysets/
class SmartCachingQuerySet(QuerySet):
    """
    This works pretty much exactly like a regular queryset
    except that when you pickle it, it does not fully evaluate
    itself, instead it evaluates DEFAULT_PREFETCH_COUNT
    records.
    """
    DEFAULT_PREFETCH_COUNT = 100
    def __init__(self, *args, **kwargs):
        self.cached_count = None
        super(SmartCachingQuerySet, self).__init__(*args, **kwargs)
        
    def __getstate__(self):
        """
        Override the default behavior of the Django QuerySet
        to only partially evaluate before pickling.
        """
        if not self._result_cache:
            self.prefetch()

        #We need to cache the count. Note, we might be
        #able to be smarter about this but why bother?
        self.count()
        
        obj_dict = self.__dict__.copy()
        obj_dict['_iter'] =  None
        return obj_dict

    def __setstate__(self, in_dict):
        """
        Restore the iterator and set the the limits.
        """
        self.__dict__ = in_dict
        self.__dict__['_iter'] = self.iterator()
        self.__dict__['query'].set_limits(low=len(self.__dict__['_result_cache']))        

    def prefetch(self, num_to_prefetch=None):
        """
        Use Django's built in functionality to prefetch
        a number of content models from the db
        """
        self.__iter__()
        self._fill_cache(num_to_prefetch or self.DEFAULT_PREFETCH_COUNT)

    def count(self):
        if self.cached_count:
            return self.cached_count

        self.cached_count = self.query.get_count(using=self.db)
        return self.cached_count

    def _filter_or_exclude(self, negate, *args, **kwargs):
        """
        Override the normal behavior of filter_or_exclude which 
        would check if limits has been set and return an error.
        Since we're handling this issue in _clone, we don't
        need to do the check.
        """
        clone = self._clone()
        if negate:
            clone.query.add_q(~Q(*args, **kwargs))
        else:
            clone.query.add_q(Q(*args, **kwargs))
        
        return clone
            
    def order_by(self, *field_names):
        """
        Override order_by for the same reason we overrode _filter_or_exclude
        """
        qs = self._clone()
        return super(SmartCachingQuerySet, qs).order_by(*field_names)

    def _clone(self, klass=None, setup=False, **kwargs):
        #Store these values and clear them so we can safely clone.
        query_limits = (self.query.low_mark, self.query.high_mark)
        result_cache = self._result_cache
        self.query.clear_limits()
        self._result_cache = None
        cloned_qs = super(SmartCachingQuerySet, self)._clone(klass, setup, **kwargs)

        #Restore stuff.
        self.query.set_limits(*query_limits)
        self._result_cache = result_cache
        return cloned_qs

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

    # Now we want to add additional events for the recommended events using the
    # recommend function (can't do two POST requests)
    recommended = recommend(event)

    template_context = {'event': event,
                        'address': address,
                        'recommended_list': recommended}

    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@csrf_exempt
def create_event(request):
     if request.user.is_authenticated():
         if request.POST:
              template = "text.html"
              template_context = {}

              try:
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
                  eFree = request.POST.get('free')
                  eNeighborhood = request.POST.get('location')
                  eCategoriesString = request.POST.get('categories')
                  eimage = request.FILES.get('image')

                  startDateTime = datetime.strptime(eStartDateTimeString, "%m/%d/%Y %I:%M %p")
                  endDateTime = datetime.strptime(eEndDateTimeString, "%m/%d/%Y %I:%M %p")

                  if eFree == "1":
                      eFreeBool = True
                  else:
                      eFreeBool = False

                  u = request.user

                  # Check to see if the event has already been created (search by user and by event name)
                  # If so, we should really jsut tell the user that a similar event has been created
                  # and that they should go edit that event rather than create a new one.
                  overwrite = request.POST.get('overwrite')

                  hasEvent = Event.objects.filter(name__iexact=eName, poster=u)

                  if hasEvent:
                      if overwrite == "false":
                          template = 'text.html'
                          template_context = {'text': 'exists'}
                          request_context = RequestContext(request, template_context)
                          return render_to_response(template, request_context)
                      elif overwrite == "true":
                          # TODO: Call edit event function here with the new information!!!!!

                          eid = hasEvent[0].id

                          template_context = {'text': eid}
                      else:
                          template_context = {'text': 'exception'}                          
                          
                  else:

                      eCategories = eCategoriesString.split(',')
              
                      n = Neighborhoods(id=eNeighborhood)
                      e = Event(start_date=startDateTime, end_date=endDateTime, name=eName, 
                                poster=u, description=eDesc, free=eFreeBool, neighborhood=n,
                                cost_max=eMaxCost, cost_min=eMinCost, venue=eVenue, url=eUrl,
                                street=eStreet, city=eCity, state=eState, zipcode=eZipcode, image=eimage)
              
                      e.save()

                      if eCategories:
                          for categoryNum in eCategories:
                              category = Categories.objects.get(id=categoryNum)
                              e.categories.add(category)

                      # Well, we created the event so all we really need to do is to               
                      # is just return the id so that we can redirect to the event page.
                      eid = Event.objects.get(name__iexact=eName).id

                      template_context = {'text': eid}
         
              except (Exception, IntegrityError) as e:
                  template_context = {'text': 'exception'}

              request_context = RequestContext(request, template_context)
              return render_to_response(template, request_context)
         else:
              template = 'text.html'
              template_context = {}
              request_context = RequestContext(request, template_context)
         
              return render_to_response(template, request_context)

def follow_event(request, event_id):
    template_context = {}
    if request.user.is_authenticated():
        event_id = int(event_id)
        event = get_object_or_404(Event, id=event_id)
        event.add_follower(request.user)
        event.save()
        template_context['text'] = '1'
    template = 'text.html'
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

@csrf_exempt
def testfilter(request):
    if request.POST:
        neighborhoods = request.POST.get('locations')
        categories = request.POST.get('categories')
        keywords = request.POST.get('keywords')
        neighborhoods_array = neighborhoods.split(',')
        categories_array = categories.split(',')
        keywords_array = keywords.split(',')
        event_list = SmartCachingQuerySet(model=Event)#Event.objects.all()
        #if date!=null:
        #     date_field = datetime.strptime(date, '%b %d %Y') 
        #    event_list = event_list.filter(start_date__lte=date_field,
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
        
#        qs = SmartCachingQuerySet(model=Event)
#        pickle_str = cPickle.dumps(event_list)
#        event_list = SmartCachingQuerySet(event_list)
        key = "filter-" + str(datetime.now())
        old_key = key
        while not cache.add(key, event_list):
            # Cache collision, add a random number to key
            key = old_key + str(random.randrange(0, 10000000))
        
        template_context = {'text': str(event_list.count()) + "," + key}
    else:
        template_context = {'text': ''}
    
    template = 'text.html'
    request_context = RequestContext(request, template_context)    
    return render_to_response(template, request_context)

@csrf_exempt
def get_events(request):
    if request.POST:
        key = request.POST.get('pickle_str')
        last_index = int(request.POST.get('last_index'))
        next_index = int(request.POST.get('next_index'))
        qs = cache.get(key)
        event_list = []
        event_list = qs[last_index:next_index]
#        counter = 0;
#        for i,v in enumerate(qs):
#            event_list.append(v)
#            counter += 1
#            if counter == 2:
#                break
    
#        cache.set(key, qs)
        template = 'eventlist.html'
        template_context = {'latest_event_list': event_list}
        
    else:
        template = '404.html'
        template_context = {}
        
    request_context = RequestContext(request, template_context)
    return render_to_response(template, request_context)

'''
Function that finds similar events to the event that is provided (included in the
post request arguments). Can also work like the "filterlist" functionality by providing
the page of events that needs to be displayed (given lots of events)
'''
def recommend(event):
    event_list = Event.objects.all()

    # TODO: Determine better recommendation algorithm than just similar 
    #       categories/locations (suggestion would be from user following)

    # Do reverse lookup of categories and neighborhood with Q object.
    categories = event.categories.all()
    neighborhood = event.neighborhood.name

    # Filter by neighborhood
    q = Q(neighborhood__name__exact=neighborhood)

    # Filter by categories.
    if len(categories) > 0:
        for category in categories[0:]:
            name = category.name
            q.add(Q(categories__name__exact=name),Q.OR)

    event_list = event_list.filter(q).distinct()

    # TODO: Determine number of elements to return and how to generate them

    # Now get 5 random elements from the search and then return as recommended
    event_list = event_list.exclude(name__exact=event.name).exclude(end_date__lt=datetime.now())[:100]
    result = []

    if event_list:
        list_max = len(event_list)
        numbers = []

        number = random.randint(0,list_max-1)

        for i in range(0,min(5, list_max)):
            while number in numbers:
                number = random.randint(0,list_max-1)
        
            numbers.append(number)
            result.append(event_list[number])
    
    return result

@csrf_exempt
def delete_event(request):
    if request.user.is_authenticated():
        template = 'text.html'
        if request.POST:
            event_id = request.POST.get('id')
            event = get_object_or_404(Event, id=event_id)
            event.delete()
        
            template_context = {'text': "1"}
            request_context = RequestContext(request, template_context)
            return render_to_response(template, request_context)
        else:
            template_context = {}
            request_context = RequestContext(request, template_context)
            return render_to_response(template, request_context)

@csrf_exempt
def edit_event(request):
    if request.user.is_authenticated():
        template = 'text.html'
        if request.POST:
            eID = request.POST.get('id')
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
            eFree = request.POST.get('free')
            eNeighborhood = request.POST.get('location')
            eCategoriesString = request.POST.get('categories')
            eimage = request.FILES.get('image')
            
            startDateTime = datetime.strptime(eStartDateTimeString, "%m/%d/%Y %I:%M %p")
            endDateTime = datetime.strptime(eEndDateTimeString, "%m/%d/%Y %I:%M %p")
            
            eCategories = eCategoriesString.split(',')
            
            if eFree == "1":
              eFreeBool = True
            else:
              eFreeBool = False
            
            n = Neighborhoods(id=eNeighborhood)
            
            e = get_object_or_404(Event, id=eID)
            
            e.name = eName;
            e.description = eDesc;
            e.start_date = startDateTime;
            e.end_date = endDateTime;
            e.last_modified = datetime.now();
            e.free = eFreeBool;
            e.neighborhood = n;
            e.cost_max = eMaxCost;
            e.cost_min = eMinCost;
            e.venue = eVenue;
            e.url = eUrl;
            e.street = eStreet;
            e.city = eCity;
            e.state = eState;
            e.zipcode = eZipcode;
            e.image = eimage;
            
            if eCategories:
                e.categories.clear()
                for categoryNum in eCategories:
                    category = Categories.objects.get(id=categoryNum)
                    e.categories.add(category)
                    
            e.save()
                    
            template_context = {'text': "1"}
            request_context = RequestContext(request, template_context)
            
            return render_to_response(template, request_context)
        else:
            template_context = {}
            request_context = RequestContext(request, template_context)
            
            return render_to_response(template, request_context)
