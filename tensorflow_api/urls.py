from django.conf.urls import url

from . import views

app_name = 'tensorflow_api'
urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^validation/$', views.validation, name='validation'),
	url(r'^scan/$', views.scan, name='scan'),
	url(r'^items/$', views.items, name='items'),
]
