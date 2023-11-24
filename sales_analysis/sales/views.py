from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from formtools.wizard.views import SessionWizardView

from .models import *
from .forms import *

def show_address_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('add_address')

def show_customer_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('customer')

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

class AddCustomerWizardView(SessionWizardView):
    form_list = [CustomerForm, AddressForm]
    template_name = "add_customer.html"
    condition_dict = {"1": show_address_form}

    def done(self, form_list, **kwargs):
        customer_form = form_list[0]
        if customer_form.cleaned_data.get('add_address'):
            customer = customer_form.save(commit = False)
            address = form_list[1].save()
            customer.address = address
            customer.save()
        else:
            customer_form.save()
        return redirect('/success')

class AddOrderCreateView(SessionWizardView):
    form_list = [OrderForm, DeliveryAddressForm,OrderProductForm]
    template_name = "add_order.html"
    context = {"customer":'dsafdsgfd'}

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'DeliveryAddressForm':
            print('duuuuuuuuuuuuuuuuupaaaaaaaaaaaaaaaa')
            context.update({'customer': show_customer_form})
        return context

    def done(self,form_list,**kwargs):
        return redirect('/success')




