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
            add_address = form.cleaned_data.get('add_address')
            if add_address:
                postal_code = form.cleaned_data.get('postal_code')
                city = form.cleaned_data.get('city')
                street = form.cleaned_data.get('street')
                building_number = form.cleaned_data.get('building_number')
                local_number = form.cleaned_data.get('local_number')
                address = Address(
                    postal_code= postal_code,
                    city=city,
                    street=street,
                    building_number=building_number,
                    local_number=local_number
                )
                address.save()
                customer = form.save(commit=False)
                customer.address = address
                customer.save()
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)



