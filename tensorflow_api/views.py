from django.shortcuts import render
from django.http import HttpResponse
from .models import ScannedItem

def index(request):
	items = ScannedItem.objects.order_by('-scanned_on')
	context = { 'items' : items }

	return render(request, 'tensorflow_api/index.html', context)

def scan(request):
	return render(request, 'tensorflow_api/scan.html')
