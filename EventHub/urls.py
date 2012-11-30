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
    url(r'^dummy$', 'direct_to_template', {'template': 'dummy.html'}),
    url(r'^dummyfilter$', 'direct_to_template', {'template': 'events/filter-dummy.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('accounts.views',
    url(r'^register$', 'register'),
    url(r'^resend$', 'resend_key'),
    url(r'^login$', 'user_login'),
    url(r'^logout$', 'user_logout'),
    url(r'^loginfb$', 'login_facebook'),
    #url(r'^connect$', 'connect'),
    url(r'^confirm/(?P<activation_key>.*)$', 'confirm'),
    url(r'^mypage$', 'dashboard'),
    url(r'^forgot$', 'forgot_password'),
    url(r'^reset/(?P<key>.*)$', 'reset_password'),
    url(r'^edit_profile$', 'edit_profile'),
)

urlpatterns += patterns('events.views',
    url(r'^$', 'index'),
    url(r'^index$', 'index'),
    url(r'^eventlist$', 'eventlist'),
    url(r'^filterlist$', 'filterlist'),
    #url(r'^search_event$', 'search_event'),
    url(r'^create_event$', 'create_event'),
    url(r'^event/(?P<event_id>.*)$', 'event'),
    url(r'^follow/(?P<event_id>.*)$', 'follow_event'),
    url(r'^unfollow/(?P<event_id>.*)$', 'unfollow_event'),
    url(r'^testfilter$', 'testfilter'),
    url(r'^getevents$', 'get_events'),
    url(r'^delete_event$', 'delete_event'),
    url(r'^edit_event$', 'edit_event'),
    url(r'^get_event_info$', 'get_event_info'),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT})
)


