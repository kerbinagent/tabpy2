from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tabpy2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/',include('registration.urls')),
    url(r'^feedback/',include('feedback.urls')),
    url(r'^admpanel/',include('admpanel.urls')),
    url(r'^$',include('tournament.urls')),
    url(r'^tournament/', include('tournament.urls')),
)
