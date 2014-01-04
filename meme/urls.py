from django.conf.urls import patterns, include, url

from meme import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^api/front', views.api_front, name='api_front'),
)
