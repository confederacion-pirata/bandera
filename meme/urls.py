from django.conf.urls import patterns, include, url

from meme import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^bandera/api/supporter/confirm/(?P<token>\w+)', views.confirm, name='confirm'),
	url(r'^bandera/api/supporter', views.supporter, name='supporter'),
	url(r'^bandera/api/candidate', views.candidate, name='candidate'),
	url(r'^candidates_json', views.candidates_json, name='candidates_json'),
	url(r'^bandera/api/member', views.member, name='member'),
	url(r'^thanks$', views.thanks, name='thanks'),
	url(r'^calendar$', views.calendar, name='calendar'),
	url(r'^manifesto$', views.manifesto, name='manifesto'),
	url(r'^tos$', views.tos, name='tos'),
	url(r'^ideas$', views.ideas, name='ideas'),
	url(r'^join-us$', views.join_us, name='join_us'),
	url(r'^ceep$', views.document, name='ceep'),
	url(r'^candidates/(?P<c_id>\d+)', views.candidate_page, name='candidate'),
	url(r'^candidates$', views.candidates, name='candidates'),
	url(r'^candidates/first$', views.candidates_first, name='candidates_first'),
)
handler403 = 'meme.views.custom_403'
handler404 = 'meme.views.custom_404'
handler500 = 'meme.views.custom_500'
