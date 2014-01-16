# -*- coding: utf-8 -*-

from django.forms import * 
from webshop.models import *

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['username', 'content', 'rating']
		labels = {
			'username': u'Ime',
			'content': u'Sadržaj',
			'rating': u'Ocjena'
		}
		widgets = {
			'username': TextInput()
		}

class OrderForm(ModelForm):
	class Meta:
		model = Order
		exclude = ['pub_date', 'server']
		labels = {
			'address': u'Adresa dostave',
			'floor': u'Kat',
			'contact_phone': u'Broj telefona',
			'contact_email': u'e-mail',
			'payment_type': u'Način plaćanja'
		}
		widgets = {
			'address': TextInput(),
			'floor': TextInput(),
			'contact_phone': TextInput(),
			'contact_email': TextInput(),
		}

		def __init__(self, *args, **kwargs):
			super(OrderForm, self).__init__(*args, **kwargs)
			self.fields['payment_type']=forms.ModelChoiceField(queryset=Order.objects.all())
