from django.conf.urls import patterns,url

from feedback import views
urlpatterns=patterns('',
        url(r'^$',views.judge_feedback,name='feedback_for_judge'),
        url(r'^feedback-success$',views.feedback_complete,name='feedback_success'),)
