from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Ingredients)
admin.site.register(MenuItem)
admin.site.register(User)
admin.site.register(ProductCart)
admin.site.register(Order)
admin.site.register(OrderItem)