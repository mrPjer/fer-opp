from django.contrib import admin
from webshop.models import *

admin.site.register(ShopInfo)
admin.site.register(Comment)
admin.site.register(Meal)
admin.site.register(PaymentType)
admin.site.register(Order)
admin.site.register(OrderedMeal)
admin.site.register(MealCategory)

