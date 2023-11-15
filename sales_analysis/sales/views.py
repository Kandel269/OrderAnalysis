from django.shortcuts import render
from .models import *

def home(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'aa.html', context)