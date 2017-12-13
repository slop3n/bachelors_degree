from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.utils import timezone
from django.core import serializers
from django.core.serializers.json import Serializer as Builtin_Serializer
from django.core.files.storage import FileSystemStorage
from .models import ScannedItem
from .tensorflow import label_image
from . import email_service

def index(request):
	return render(request, 'tensorflow_api/index.html')

def items(request):
	items =  ScannedItem.objects.order_by('-scanned_on')
	output = { 'data': list(items.values()), 'success':True, 'total':4 }

	return JsonResponse(output, safe=False)

def detail(request, item_id):
	return render(request, 'tensorflow_api/detail.html', { 'item': item })

def scan(request):
	file = request.FILES['image']
	fs = FileSystemStorage();
	filename = fs.save('images/'+file.name, file)
	uploaded_file_url = fs.url(filename)

	categories = label_image.classify(uploaded_file_url)

	if categories:
		first = categories[0]
		percentage = round(first['probability'] * 100, 2)

		item = ScannedItem(label=first['label'], probability=percentage, scanned_on=timezone.now())
		item.save()

		text = 'a new image has been uploaded, it has a chance of being one of the follwing:\n'

		for category in categories:
			percentage = round(category['probability'] * 100, 2)
			text += '{0} with chance {1}'.format(category['label'], percentage)
		
		email_service.sendmail('slop3n@gmail.com', 'new image', text)

	return HttpResponseRedirect(reverse('tensorflow_api:index'))
