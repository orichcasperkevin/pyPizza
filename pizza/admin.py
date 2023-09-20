from django.contrib import admin
from pizza.models import Crust,Topping,Order,OrderMessageConfig
# Register your models here.
admin.site.register(Crust)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderMessageConfig)
