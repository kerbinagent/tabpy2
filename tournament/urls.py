from django.conf.urls import patterns,url

from tournament import views
urlpatterns=patterns('',
        url(r'^$',views.index,name='index'),
        url(r'^judge/(?P<judge_code>[\w\-]+)/$',views.judge,name='judge'),
        url(r'^initiate_matchup$',views.matchup, name="matchup"),
        url(r'^matchup/(?P<round_number>[\w\-]+)/$',views.show_matchup,name='show_matchup'),)
