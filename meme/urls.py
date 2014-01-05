from django.conf.urls import patterns, include, url

from meme import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^api/supporter', views.supporter, name='supporter'),
	url(r'^api/candidate', views.candidate, name='candidate'),
	url(r'^thanks$', views.thanks, name='thanks'),
)
