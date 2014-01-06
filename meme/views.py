# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from bandera import settings
from forms import SupporterForm, CandidateForm
from models import Supporter

def index(request):
	return render(request, 'index.html', {'form': SupporterForm(), 'request': request})

def supporter(request):
	if request.method == 'POST':
		form = SupporterForm(request.POST, request.FILES)
		if form.is_valid():
			supporter = form.save()
			if form.cleaned_data['ok_candidate']:
				return HttpResponseRedirect('%s?token=%s' % (reverse('candidate'), supporter.token))
			send_confirmation_email(supporter)
			return HttpResponseRedirect(get_thanks_destination())
		return render(request, 'index.html', {'form': form, 'request': request})
	return HttpResponseRedirect('http://piratas2014.eu/')

def candidate(request):
	form = CandidateForm()
	token = None
	if request.method == 'POST':
		form = CandidateForm(request.POST, request.FILES)
		if form.is_valid():
			candidate = form.save()
			send_confirmation_email(candidate.supporter)
			return HttpResponseRedirect(get_thanks_destination())
		token = form.data['token']
	else:
		token = request.GET.get('token')
	if not token:
		return PermissionDenied
	form.set_token(token)
	return render(request, 'candidate.html', {'form': form, 'request': request})

def confirm(request, token = None):
	if not token:
		return PermissionDenied
	supporter = Supporter.objects.filter(token__iexact=token)
	if not supporter:
		return PermissionDenied
	data = supporter[0]
	if data.confirmed == True:
		return HttpResponseRedirect(get_thanks_destination())
	data.confirmed = True
	data.save()
	return render(request, 'confirm.html', {'request': request})

def thanks(request):
	return render(request, 'thanks.html', {'request': request})

def calendar(request):
	return render(request, 'calendar.html', {'request': request})

def get_thanks_destination():
	if settings.DEBUG:
		return reverse('thanks')
	return 'http://piratas2014.eu/thanks'

def send_confirmation_email(supporter):
	context = {
		'token': supporter.token,
	}
	message = render_to_string('confirmation.txt', context)
	send_mail(
		'Confirmación #SeBuscanPiratas - Confederación Pirata',
		message,
		settings.DEFAULT_FROM_EMAIL,
		[supporter.email]
	)

def manifesto():
	pass

def privacy():
	pass

def tos():
	pass

def custom_403():
	return render(request, '403.html', {})

def custom_404():
	return render(request, '404.html', {})

def custom_500():
	return render(request, '500.html', {})
