# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import *
from .forms import * 
import datetime
import mimetypes


def index(request):
        today = datetime.date.today()

	context = dict(map(lambda i: [i.key, i.value], ShopInfo.objects.all()))
        context['num_orders_month'] = Order.objects.filter(
            pub_date__year = today.year,
            pub_date__month = today.month
        ).count()
        print(context['num_orders_month'])
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
	cart = request.session.get('cart', {})
	meals = [(Meal.objects.get(pk=k), v) for k, v in cart.items()]

	return render(request, 'meal/index.html', {
		'categories': MealCategory.objects.all().order_by('name'),
		'meals': meals
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
	total = sum(map(lambda (m, c): m.price * c, meals))
        minimum = float(ShopInfo.objects.get(key='min_order').value)
	delivery = float(ShopInfo.objects.get(key='delivery_cost').value)
	full = total + delivery

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			order = form.save()

			for (meal, count) in meals:
				for i in range(0, count):
					orderedMeal = OrderedMeal()
					orderedMeal.meal = meal
					orderedMeal.order = order
					orderedMeal.save()

			request.session.__setitem__('cart', {})

                        mail = render_to_string('order/textual.html', {
                            'order': order,
                            'meals': map(lambda (m,c):m, meals),
                            'total': full,
                            'delivery': delivery
                        })

                        send_mail(u'Vaša narudžba (#{})'.format(order.id), mail, 'opp.sedmica@gmx.com', [order.contact_email])

			return redirect('webshop.views.cart_success')
	else:
		form = OrderForm()

	return render(request, 'cart/index.html', {
		'meals': meals,
		'total': total,
		'form': form,
		'delivery': delivery,
		'full': full,
                'minimum': minimum 
	})

def cart_success(request):
	return render(request, 'cart/success.html')

@login_required
def orders(request):
	return render(request, 'order/index.html', {
		'open_orders': Order.objects.filter(server__isnull=True).order_by('-pub_date'),
		'closed_orders': Order.objects.filter(server__isnull=False).order_by('-pub_date') 
	})

@login_required
def take_order(request, orderId):
    order = get_object_or_404(Order, pk=orderId)
    order.server = request.user
    order.save()
    return redirect('webshop.views.orders')

@login_required
def order_details(request, orderId):
    order = get_object_or_404(Order, pk=orderId)
    meals = map(lambda om: om.meal, list(order.orderedmeal_set.all()))
    total = sum(map(lambda m:m.price, meals))
    return render(request, 'order/detail.html', {
        'order': order,
        'meals': meals,
        'total': total
    })

@login_required
def order_as_txt(request, orderId):
    order = get_object_or_404(Order, pk=orderId)
    name = ShopInfo.objects.get(key="name").value
    meals = map(lambda om: om.meal, list(order.orderedmeal_set.all()))
    total = sum(map(lambda m:m.price, meals))
    return render(request, 'order/textual.html', {
        'order': order,
        'meals': meals,
        'total': total,
        'delivery': float(ShopInfo.objects.get(key='delivery_cost').value)
    }, content_type='text/plain; charset=utf-8')

@login_required
def staff(request):
    staff = User.objects.order_by('username')
    wc = map(lambda u: (u, Order.objects.filter(server=u).count()), staff)

    return render(request, 'staff/index.html', {
        'staff': wc 
    })
