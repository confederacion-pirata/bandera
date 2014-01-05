from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from bandera import settings
from .forms import SupporterForm, CandidateForm

def index(request):
	return render(request, 'index.html', {'form': SupporterForm()})

def supporter(request):
	if request.method == 'POST':
		form = SupporterForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			if form.cleaned_data['ok_candidate']:
				return HttpResponseRedirect(reverse('candidate'))
			return HttpResponseRedirect(get_thanks_destination())
		return render(request, 'index.html', {'form': form})
	return HttpResponseRedirect(reverse('index'))

def candidate(request):
	form = CandidateForm()
	if request.method == 'POST':
		form = CandidateForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(get_thanks_destination())
	return render(request, 'candidate.html', {'form': form})

def thanks(request):
	return render(request, 'thanks.html', {})

def get_thanks_destination():
	if settings.DEBUG:
		return reverse('thanks')
	return 'http://piratas2014.eu/thanks'
