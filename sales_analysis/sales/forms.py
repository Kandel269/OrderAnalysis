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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('add_address') and not (cleaned_data.get('postal_code') and cleaned_data.get('city')  and cleaned_data.get('street')  and cleaned_data.get('building_number')  and cleaned_data.get('local_number')):
    #         self.add_error('postal_code',"If 'Add address' is enabled, you must complete the fields below.")
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'e_mail')

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(max_length=255)
    order_noters = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Order
        fields = ('order_status', 'customer','ordered_date')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
    # postal_code = forms.CharField(max_length=10, required=False)
    # city = forms.CharField(max_length=255, required=False)
    # street = forms.CharField(max_length=255, required=False)
    # building_number = forms.CharField(max_length=255, required=False)
    # local_number = forms.CharField(max_length=255, required=False)
