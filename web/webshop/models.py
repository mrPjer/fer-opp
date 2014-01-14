# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
		verbose_name = u'komentar'
		verbose_name_plural = u'komentari'

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
		verbose_name = u'kategorija jela'
		verbose_name_plural = u'kategorije jela'

	name = models.TextField()
    
	def __unicode__(self):
		return self.name

class Meal(models.Model):
	class Meta:
		verbose_name = u'jelo'
		verbose_name_plural = u'jela'

	name = models.TextField()
	price = models.FloatField()
	available = models.BooleanField(default = True)
	on_sale = models.BooleanField(default = False)
	times_ordered = models.PositiveIntegerField(default = 0)
	category = models.ForeignKey(MealCategory)

class PaymentType(models.Model):
	class Meta:
		verbose_name = u'način plaćanja'
		verbose_name_plural = u'načini plaćanja'

	name = models.TextField()

	def __unicode__(self):
		return self.name

class Order(models.Model):
	class Meta:
		verbose_name = u'narudžba'
		verbose_name_plural = u'narudžbe'

	address = models.TextField()
	floor = models.TextField()
	contact_phone = models.TextField()
	contact_email = models.TextField()
	payment_type = models.ForeignKey(PaymentType)
	pub_date = models.DateTimeField(auto_now = True)
    
	def price(self):
		return 42

	def __unicode__(self):
		return u'{} @ {}'.format(address, pub_date)
    # TODO - person who will deliver

class OrderedMeal(models.Model):
    order = models.ForeignKey(Order)
    meal = models.ForeignKey(Meal)

