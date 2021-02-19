from django import forms
from .models import OrderInformation


class OrderingForm(forms.ModelForm):
    class Meta:
        model = OrderInformation
        fields = ('full_name', 'email_address', 'contact_number',
                  'street_name_1', 'street_name_2',
                  'town_or_city', 'postal_code', 'county',)
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email_address': 'Email Address',
            'contact_number': 'Contact Number',
            'town_or_city': 'Town or City',
            'street_name_1': 'Street Name 1',
            'street_name_2': 'Street Name 2',
            'postal_code': 'Postal Code',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
