from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core import serializers
from django.core.serializers.json import Serializer as Builtin_Serializer
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from .models import ScannedItem
from .tensorflow import label_image
from . import email_service
import datetime

def index(request):
	return render(request, 'tensorflow_api/index.html', { 'validation': False })

def validation(request):
	return render(request, 'tensorflow_api/index.html', { 'validation' : True })

def items(request):
	items =  ScannedItem.objects.order_by('-scanned_on')
	output = { 'data': list(items.values()), 'success':True, 'total':items.count() }

	return JsonResponse(output, safe=False)

@csrf_exempt
def scan(request):
	if not request.FILES:
		return HttpResponseRedirect(reverse('tensorflow_api:validation'))
	file = request.FILES['image']
	if not (file.name.endswith('.jpg') or file.name.endswith('.jpeg') or file.name.endswith('.png')):
		return HttpResponseRedirect(reverse('tensorflow_api:validation'))

	fs = FileSystemStorage();
	filename = fs.save('images/'+file.name, file)
	uploaded_file_url = fs.url(filename)

	category = label_image.classify(uploaded_file_url)
	if category:
		percentage = round(category['probability'] * 100, 5)

		if not ScannedItem.objects.filter(label=category['label'], probability=percentage, 
			scanned_on__gt=datetime.datetime.today()-datetime.timedelta(days=1)).exists():
			item = ScannedItem(label=category['label'], probability=percentage, scanned_on=timezone.now())
			item.save()

			subject = 'new image ' + category['label']
			text = 'a new image has been uploaded, it has a ' + str(round(percentage, 3)) + ' percent chance of being ' + category['label']

			email_service.sendmail('slop3n@gmail.com', subject, text, uploaded_file_url)
	# else:
		# email_service.sendmail('slop3n@gmail.com', 'new image', 'an image has been sent from the raspberry but it was not recognized')

	return HttpResponseRedirect(reverse('tensorflow_api:index'))
