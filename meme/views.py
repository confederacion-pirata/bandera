from django.shortcuts import render
from form import FrontForm

def index(request):
	return render(request, 'index.html', {'form': FrontFrom()})

def api_front(request):
	return render(request, 'front.html', {})
