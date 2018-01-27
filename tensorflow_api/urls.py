from django.conf.urls import url

from . import views
# дефиниция на заявките които ще се прихващат от Django и методите към 
# които ще се насочват тези заявки
app_name = 'tensorflow_api'
urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^scan/$', views.scan, name='scan'),
	url(r'^items/$', views.items, name='items'),
]
