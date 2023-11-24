from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from formtools.wizard.views import SessionWizardView

from .models import *
from .forms import *

def show_address_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('add_address')

def use_customer_address_or_show_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('1') or {}
    return cleaned_data.get('use_customer_address')

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
    form_list = [OrderForm, ChooseDeliveryAddressForm, AddressForm, OrderProductForm]
    template_name = "add_order.html"
    condition_dict = {"2": use_customer_address_or_show_form}

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            customer_pk = self.storage.get_step_data('0')['0-customer']
            customer = get_object_or_404(Customer, pk=customer_pk)

            context.update({'customer': customer})
        return context

    def done(self,form_list,**kwargs):
        order_form = form_list[0]
        order_product_form = form_list[-1]
        choose_address_form = form_list[1]

        order_notes = order_form.cleaned_data.get('order_notes')
        order_product = order_product_form.save(commit = False) #order_detail
        order = order_form.save(commit=False) #orderdetail

        if not choose_address_form.cleaned_data.get('use_customer_address'):
            customer = order_form.cleaned_data.get('customer')
            address = customer.address
        else:
            address_form = form_list[-2]
            address = address_form.save()

        order_detail = OrderDetail.objects.create(delivery_address = address, order_notes = order_notes)
        order.orderdetail = order_detail
        order_product.order_detail = order_detail

        order_product.save()
        order.save()
        return redirect('/success')




