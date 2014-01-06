from django.conf.urls import patterns, include, url

from meme import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^bandera/api/supporter/confirm/(?P<token>\w+)', views.confirm, name='confirm'),
	url(r'^bandera/api/supporter', views.supporter, name='supporter'),
	url(r'^bandera/api/candidate', views.candidate, name='candidate'),
	url(r'^thanks$', views.thanks, name='thanks'),
	url(r'^calendar$', views.calendar, name='calendar'),
	url(r'^manifesto$', views.manifesto, name='manifesto'),
	url(r'^privacy$', views.privacy, name='privacy'),
	url(r'^tos$', views.tos, name='tos'),
	url(r'^ideas$', views.ideas, name='ideas'),
	url(r'^join-us$', views.join_us, name='join_us'),
	url(r'^ceep$', views.document, name='ceep'),
)
handler403 = 'meme.views.custom_403'
handler404 = 'meme.views.custom_404'
handler500 = 'meme.views.custom_500'
