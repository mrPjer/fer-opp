# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput 
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
