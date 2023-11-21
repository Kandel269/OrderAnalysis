from django import forms

from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    postal_code = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    building_number = forms.CharField(max_length=255, required=False)
    local_number = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Customer
        fields = ('name', 'phone', 'e_mail')

