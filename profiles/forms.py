from django import forms
from .models import UserProfile


class UsersProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_full_name': 'Full Name',
            'default_email_address': 'Email Address',
            'default_contact_number': 'Contact Number',
            'default_town_or_city': 'Town or City',
            'default_street_name_1': 'Street Name 1',
            'default_street_name_2': 'Street Name 2',
            'default_county': 'County',
            'default_postal_code': 'Postal Code',
        }

        self.fields['default_contact_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
