from django.shortcuts import render
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import CommentForm 
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
