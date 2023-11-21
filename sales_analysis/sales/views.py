from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView

from .models import *
from .forms import *

class FormSuccessView(View):
    def get(self, request):
        return render(request,'success.html')

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')

class AddProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = 'success'

class AddCustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "add_customer.html"
    success_url = 'success'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            for i in form:
                print(i)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
