from django.conf.urls import patterns, url
from webshop import views

urlpatterns = patterns('',
	url(r'^komentari/$', views.comments, name='comments'),
	url(r'^meni/$', views.menu, name='menu'),
	url(r'^kosarica/$', views.cart, name='cart'),
	url(r'^meni/(?P<mealId>.+)/dodaj$', views.add_to_cart, name='add_to_cart'),
	url(r'^meni/(?P<mealId>.+)/makni$', views.remove_from_cart, name='remove_from_cart'),
	url(r'^meni/(?P<mealId>.+)/makni_jedan$', views.subtract_from_cart, name='subtract_from_cart'),
	url(r'^img/(?P<filename>.+)$', views.image, name='image'),
	url(r'^$', views.index, name='index'),
)
