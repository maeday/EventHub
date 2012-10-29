from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    # Examples:
    # url(r'^$', 'EventHub.views.home', name='home'),
    # url(r'^EventHub/', include('EventHub.foo.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^full-view$', 'direct_to_template', {'template': 'full-view.html'}),
    url(r'^my-events$', 'direct_to_template', {'template': 'my-events.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('accounts.views',
    url(r'^register$', 'register'),
    url(r'^login$', 'user_login'),
    url(r'^logout$', 'user_logout'),
)

urlpatterns += patterns('events.views',
    url(r'^$', 'index'),
    url(r'^index$', 'index'),
<<<<<<< HEAD
    url(r'^eventlist$', 'eventlist'),
=======
    url(r'^create_event$', 'create_event'),
>>>>>>> Added create_event controller code
)