from django import forms
from django.forms.widgets import HiddenInput

from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    BOOL_CHOICES = [(True, "Yes"), (False, "No")]
    add_address = forms.BooleanField(
        widget = forms.RadioSelect(choices=BOOL_CHOICES),
        required=False
    )

    class Meta:
        model = Customer
        fields = ('name', 'phone', 'e_mail')

class OrderForm(forms.ModelForm):
    order_notes = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Order
        fields = ('order_status', 'customer','date_of_order','delivery_date')
        widgets = {
            'date_of_order': forms.DateInput(attrs={'type':'date'}),
            'delivery_date': forms.DateInput(attrs={'type':'date'}),
                   }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class DeliveryAddressForm(AddressForm):
    BOOL_CHOICES = [(True, "Yes"), (False, "No")]
    use_customer_address = forms.BooleanField(
        widget = forms.RadioSelect(choices=BOOL_CHOICES, attrs={'id': 'use_customer_address'}),
        required=False
    )


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ('product','quantity')

