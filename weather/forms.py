from django import forms
from .validators import validate_length

class CityForm(forms.Form):
    zipcode = forms.CharField(required=False,label='zipcode', max_length=5, validators=[validate_length], widget=forms.TextInput(attrs={'placeholder': 'Enter a US Zipcode', 'class' : 'form-control form-control-m text-center'}))