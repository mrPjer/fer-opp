from django.conf.urls import patterns, url
from webshop import views

urlpatterns = patterns('',
	url(r'^komentari/$', views.comments, name='comments'),
	url(r'^img/(?P<filename>.+)$', views.image, name='image'),
	url(r'^$', views.index, name='index'),
)
