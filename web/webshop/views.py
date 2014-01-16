from django.shortcuts import render, redirect
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import * 
import mimetypes

def index(request):
	context = dict(map(lambda i: [i.key, i.value], ShopInfo.objects.all()))
	context['payment_types'] = PaymentType.objects.all()
	context['avg_score'] = Comment.objects.all().aggregate(Avg('rating'))['rating__avg']
	if context['avg_score']:
		context['num_stars'] = int(round(context['avg_score']))
	context['discounted_meals'] = Meal.objects.filter(on_sale = True) 
	return render(request,'index.html', context)

def chunks(l, n):
	return [l[i:i+n] for i in range(0, len(l), n)]

def comments(request):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(request.path)
	else:
		form = CommentForm()
	return render(request, 'comment/index.html', {
		'comments': chunks(Comment.objects.all().order_by('-pub_date')[:20], 3),
		'form': form
	})

def image(request, filename):
	storage = DatabaseStorage(IMG_DB_OPTS)
	image_file = storage.open(filename, 'rb')

	if not image_file:
		raise Http404

	file_content = image_file.read()
	content_type, content_encoding = mimetypes.guess_type(filename)
	response = HttpResponse(content=file_content, mimetype=content_type)
	response['Content-Disposition'] = 'inline; filename=%s' % filename

	if content_encoding:
		response['Content-Encoding'] = content_encoding

	return response

def menu(request):
	return render(request, 'meal/index.html', {
		'categories': MealCategory.objects.all().order_by('name')
	})

def add_to_cart(request, mealId):
	current = request.session.get('cart', {})
	count = current.get(mealId, 0)
	current[mealId]= count + 1
	request.session.__setitem__('cart', current)
	
	return redirect('webshop.views.cart')

def subtract_from_cart(request, mealId):
	current = request.session.get('cart', {})
	if mealId in current:
		count = current.get(mealId, 0)
		count = count - 1
		if count <= 0:
			return remove_from_cart(request, mealId)
		else:
			current[mealId] = count
			request.session.__setitem__('cart', current)

	return redirect('webshop.views.cart')
	

def remove_from_cart(request, mealId):
	current = request.session.get('cart', {})
	current.pop(mealId, None)
	request.session.__setitem__('cart', current)

	return redirect('webshop.views.cart')

def cart(request):
	cart = request.session.get('cart', {})
	meals = [(Meal.objects.get(pk=k), v) for k, v in cart.items()]

	return render(request, 'cart/index.html', {
		'meals': meals,
		'total': sum(map(lambda (m, c): m.price * c, meals)),
		'form': OrderForm()
	})
