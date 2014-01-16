# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from database_storage import DatabaseStorage 

IMG_DB_OPTS = {
    'table': 'image_uploads',
    'base_url': '/webshop/img/'
}

class ShopInfo(models.Model):
	class Meta:
            verbose_name = u'informacija o dućanu'
            verbose_name_plural = 'informacije o dućanu'

	key = models.TextField(unique = True)
	description = models.TextField()
	value = models.TextField()

	def __unicode__(self):
		return u'{} = {}'.format(self.description, self.value)

class Comment(models.Model):
	class Meta:
		verbose_name = 'komentar'
		verbose_name_plural = 'komentari'

	username = models.TextField()
	pub_date = models.DateTimeField(auto_now = True)
	content = models.TextField()
	rating = models.IntegerField(null = True, blank = True, validators = [
		MaxValueValidator(5),
		MinValueValidator(1)
	])

	def __unicode__(self):
		return u'{} @ {} ({}) - {}'.format(self.username, self.pub_date, self.rating, self.content)

class MealCategory(models.Model):
	class Meta:
		verbose_name = 'kategorija jela'
		verbose_name_plural = 'kategorije jela'

	name = models.TextField()
    
	def __unicode__(self):
		return self.name

class Meal(models.Model):
	class Meta:
		verbose_name = 'jelo'
		verbose_name_plural = 'jela'

	name = models.TextField()
	price = models.FloatField()
	image = models.ImageField(
		upload_to = 'meal',
		storage=DatabaseStorage(IMG_DB_OPTS),
		blank = True
	)
	available = models.BooleanField(default = True)
	on_sale = models.BooleanField(default = False)
	times_ordered = models.PositiveIntegerField(default = 0)
	category = models.ForeignKey(MealCategory)

	def is_hot(self):
            avg = Meal.objects.all().aggregate(Avg('times_ordered'))['times_ordered__avg']
            return self.times_ordered >= 2*avg 

	def __unicode__(self):
            return u"{} - {}".format(self.category.name, self.name)

class PaymentType(models.Model):
	class Meta:
		verbose_name = 'način plaćanja'
		verbose_name_plural = 'načini plaćanja'

	name = models.TextField()

	def __unicode__(self):
		return self.name

class Order(models.Model):
	class Meta:
		verbose_name = 'narudžba'
		verbose_name_plural = 'narudžbe'

	address = models.TextField()
	floor = models.TextField()
	contact_phone = models.TextField()
	contact_email = models.TextField()
	payment_type = models.ForeignKey(PaymentType)
	pub_date = models.DateTimeField(auto_now = True)
	server = models.ForeignKey(User, blank = True, null = True)
    
	def __unicode__(self):
		return '{} @ {}'.format(self.address, self.pub_date)

class OrderedMeal(models.Model):
    order = models.ForeignKey(Order)
    meal = models.ForeignKey(Meal)

