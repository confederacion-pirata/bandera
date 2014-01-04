from django.shortcuts import render
from .forms import FrontForm

def index(request):
	return render(request, 'index.html', {'form': FrontForm()})

def api_front(request):
	return render(request, 'front.html', {})
