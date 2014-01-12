from django.forms import ModelForm, CharField
from webshop.models import *

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['username', 'content', 'rating']
