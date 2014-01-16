from django.contrib import admin
from webshop.models import *

class ShopInfoRegister(admin.ModelAdmin):
	fields = ['description', 'value']

class CommentRegister(admin.ModelAdmin):
	fields = ['username','content']

admin.site.register(ShopInfo,ShopInfoRegister)
admin.site.register(Comment,CommentRegister)
admin.site.register(Meal)
admin.site.register(PaymentType)
admin.site.register(Order)
admin.site.register(MealCategory)

