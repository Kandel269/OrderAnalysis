from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(OrderDetail)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Category)
