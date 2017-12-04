from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import email_service
from .models import ScannedItem

def index(request):
	items = ScannedItem.objects.order_by('-scanned_on')
	context = { 'items' : items }

	return render(request, 'tensorflow_api/index.html', context)

def detail(request, item_id):
	item = get_object_or_404(ScannedItem, pk=item_id)

	return render(request, 'tensorflow_api/detail.html', { 'item': item })

def scan(request):
	email_service.sendmail('slop3n@gmail.com', 'teeee', 'zezezeeze')
	return HttpResponseRedirect(reverse('tensorflow_api:index'))
