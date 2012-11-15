from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    # Examples:
    # url(r'^$', 'EventHub.views.home', name='home'),
    # url(r'^EventHub/', include('EventHub.foo.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^event$', 'direct_to_template', {'template': 'event.html'}),
    url(r'^forgot$', 'direct_to_template', {'template': 'accounts/forgot.html'}),
    url(r'^dummy$', 'direct_to_template', {'template': 'dummy.html'}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('accounts.views',
    url(r'^register$', 'register'),
    url(r'^login$', 'user_login'),
    url(r'^logout$', 'user_logout'),
    url(r'^loginfb$', 'login_facebook'),
    #url(r'^connect$', 'connect'),
    url(r'^mypage$', 'dashboard'),
)

urlpatterns += patterns('events.views',
    url(r'^$', 'index'),
    url(r'^index$', 'index'),
    url(r'^eventlist$', 'eventlist'),
    url(r'^create_event$', 'create_event'),
    url(r'^event/(?P<event_id>.*)$', 'event'),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT})
)
