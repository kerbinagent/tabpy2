from django.conf.urls import patterns,url

from tournament import views
urlpatterns=patterns('',
        url(r'^$',views.index,name='index'),
        url(r'^judge/$',views.judge,name='judge'),
        url(r'^initiate_matchup$',views.matchup, name="matchup"),
        url(r'^initiate_next/([{0-9}]+)$',views.matchup_next,name="matchup_next"),
        url(r'^show-tab$',views.show_tab, name="show_tab"),
        url(r'^breaking/(?P<admin_code>[\w\-]+)/$',views.breaking,name="breaking"),
        url(r'^matchup/(?P<round_number>[\w\-]+)/$',views.show_matchup,name='show_matchup'),)
