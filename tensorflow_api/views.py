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

# метод които ни връща основната страница на приложението
def index(request):
	return render(request, 'tensorflow_api/index.html')

# метод чрез който извличаме данните за таблицата, тези данни са сортирани по дата на сканиране
def items(request):
	items =  ScannedItem.objects.order_by('-scanned_on')
	output = { 'data': list(items.values()), 'success':True, 'total':items.count() }

	return JsonResponse(output, safe=False)

# метод към който се подава картинка за сканиране
@csrf_exempt
def scan(request):
	# прихващане на картинката и нейното запазване на сървъра
	file = request.FILES['image']
	fs = FileSystemStorage();
	filename = fs.save('images/'+file.name, file)
	uploaded_file_url = fs.url(filename)

	# извикване на невронната мрежа, като тя ни връща категорията към която попада изображението
	category = label_image.classify(uploaded_file_url)
	# прави се проверка дали категорията е различна от празно поле
	if category:
		percentage = round(category['probability'] * 100, 5)

		# прави се проверка дали има предмет със същата категория и вероятност в базата с данни 
		# за последните 24 часа
		if not ScannedItem.objects.filter(label=category['label'], probability=percentage, 
			scanned_on__gt=datetime.datetime.today()-datetime.timedelta(days=1)).exists():
			
			# ако няма такъв запис в базата данни се създава нов
			item = ScannedItem(label=category['label'], probability=percentage, scanned_on=timezone.now())
			item.save()

			# параметри за имейла който ще получи потребителя
			subject = 'new image ' + category['label']
			text = 'a new image has been uploaded, it has a ' + str(round(percentage, 3)) + ' percent chance of being ' + category['label']

			# извикване на имейл програмата
			email_service.sendmail('slop3n@gmail.com', subject, text, uploaded_file_url)

	# пренасочване към основната страница на приложението
	return HttpResponseRedirect(reverse('tensorflow_api:index'))
