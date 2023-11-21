from django import forms
from django.forms.widgets import HiddenInput

from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    add_address = forms.BooleanField(required=False, initial=False, help_text="(optional)")
    postal_code = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    building_number = forms.CharField(max_length=255, required=False)
    local_number = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('add_address') and not (cleaned_data.get('postal_code') and cleaned_data.get('city')  and cleaned_data.get('street')  and cleaned_data.get('building_number')  and cleaned_data.get('local_number')):
            self.add_error('postal_code',"If 'Add address' is enabled, you must complete the fields below.")
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'e_mail')


