from django.conf.urls import patterns,url
from admpanel import views

urlpatterns=patterns('',
        url(r'^registration',views.register,name='register'),
        url(r'^$',views.admpanel,name='admpanel'),
        url(r'^init$',views.initpanel,name='initpanel'),
        url(r'^newentry/([{0-9}]+)',views.new_entry,name='new_entry'),
        url(r'^ballot/([{0-9}]+)',views.ballot_edit,name='ballot_edit'),
        url(r'^matchup/([{0-9}]+)',views.matchup_edit,name='matchup_edit'),
        url(r'^login',views.user_login,name='login'),
        url(r'^logout',views.user_logout,name='logout'),)
