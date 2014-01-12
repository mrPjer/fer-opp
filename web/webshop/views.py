from django.shortcuts import render
from django.db.models import Avg
from django.http import HttpResponse
from .models import *
from .forms import CommentForm 

def index(request):
	context = dict(map(lambda i: [i.key, i.value], ShopInfo.objects.all()))
	context['payment_types'] = PaymentType.objects.all()
	context['avg_score'] = Comment.objects.all().aggregate(Avg('rating'))['rating__avg']
	context['discounted_meals'] = Meal.objects.filter(on_sale = True) 
	print(context)
	return render(request,'index.html', context)

def chunks(l, n):
	return [l[i:i+n] for i in range(0, len(l), n)]

def comments(request):
	return render(request, 'comment/index.html', {
		'comments': chunks(Comment.objects.all()[:20], 3),
		'form': CommentForm()
	})
