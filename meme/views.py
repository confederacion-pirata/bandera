from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from bandera import settings
from forms import SupporterForm, CandidateForm
from models import Supporter

def index(request):
	return render(request, 'index.html', {'form': SupporterForm()})

def supporter(request):
	if request.method == 'POST':
		form = SupporterForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			if form.cleaned_data['ok_candidate']:
				return HttpResponseRedirect(get_candidate_destination())
			send_confirmation_email()
			return HttpResponseRedirect(get_thanks_destination())
		return render(request, 'index.html', {'form': form})
	return HttpResponseRedirect(reverse('index'))

def candidate(request):
	form = CandidateForm()
	if request.method == 'POST':
		form = CandidateForm(request.POST, request.FILES)
		if form.is_valid():
			supporter = Supporter.objects.filter(csrf__iexact=form.data['csrfmiddlewaretoken'])
			if not supporter:
				raise PermissionDenied
			form.save()
			send_confirmation_email()
			return HttpResponseRedirect(get_thanks_destination())
	return render(request, 'candidate.html', {'form': form})

def thanks(request):
	return render(request, 'thanks.html', {})

def get_thanks_destination():
	if settings.DEBUG:
		return reverse('thanks')
	return 'http://piratas2014.eu/thanks'

def get_candidate_destination():
	if settings.DEBUG:
		return reverse('candidate')
	return 'http://piratas2014.eu/api/bandera/candidate'

def send_confirmation_email():
	pass

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
