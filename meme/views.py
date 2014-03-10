# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.core.mail import send_mail
from bandera import settings
from forms import SupporterForm, CandidateForm, MemberCandidateForm, regions
from models import Supporter, Candidate
import random
import os

@cache_page(60 * 15)
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

def member(request):
	form = MemberCandidateForm()
	if request.method == 'POST':
		form = MemberCandidateForm(request.POST, request.FILES)
		if form.is_valid():
			candidate = form.save()
			send_confirmation_email(candidate.supporter)
			return HttpResponseRedirect(get_thanks_destination())
	return render(request, 'member.html', {'form': form, 'request': request})

@cache_page(60 * 15)
def candidate_page(request, c_id):
	candidate = get_object_or_404(Candidate, pk=c_id)
	if candidate.phase != 9:
		raise Http404
	return render(request, 'candidate_page.html', {'request': request, 'c': fix_candidate(candidate)})

def resolve_region_name(region):
	return [t[1] for t in regions if t[0] == region][0]

def candidates(request):
	cq = Candidate.objects.filter(phase__lte=2)
	candidates = [fix_candidate(c) for c in cq]
	random.shuffle(candidates)
	return render(request, 'candidates.html', {'request': request, 'candidates': candidates, 'phase': 2})

def candidates_first(request):
	cq = Candidate.objects.filter(phase__exact=1)
	candidates = [fix_candidate(c) for c in cq]
	random.shuffle(candidates)
	return render(request, 'candidates.html', {'request': request, 'candidates': candidates, 'phase': 1})

def fix_candidate(c):
	if c.id == 18 or c.id == 22 or c.id == 42:
		return None
	c.supporter.region = resolve_region_name(c.supporter.region)
	c.photo = None
	photo = '%s.jpg' % c.pk
	photo_path = os.path.abspath(os.path.join(
		settings.STATIC_ROOT,
		'photos',
		photo
	))
	if os.path.isfile(photo_path):
		c.photo = photo
	return c

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

@cache_page(60 * 15)
def thanks(request):
	return render(request, 'thanks.html', {'request': request})

@cache_page(60 * 15)
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

@cache_page(60 * 15)
def manifesto(request):
	return render(request, 'manifesto.html', {'request': request})

@cache_page(60 * 15)
def tos(request):
	return render(request, 'tos.html', {'request': request})

@cache_page(60 * 15)
def ideas(request):
	return render(request, 'ideas.html', {'request': request})

@cache_page(60 * 15)
def join_us(request):
	return render(request, 'join_us.html', {'request': request})

@cache_page(60 * 15)
def document(request):
	return render(request, 'ceep.html', {'request': request})

def custom_403():
	return render(request, '403.html', {'request': request})

def custom_404():
	return render(request, '404.html', {'request': request})

def custom_500():
	return render(request, '500.html', {'request': request})
