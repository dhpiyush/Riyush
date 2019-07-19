from django import forms
from django.forms import  EmailInput, TextInput
from order.models import contact



class contactform(forms.ModelForm):
    class Meta :
        model = contact
        exclude = []
        widgets = {
                'name' : TextInput(attrs={'class': 'validate', 'required': True}),
                'number' : TextInput(attrs={'class': 'validate', 'required': True}),
                'email': EmailInput(attrs={'class': 'validate', 'required': True}),
                'message' :  TextInput(attrs={'class': 'validate', 'required': True}),
                }

        labels = {
            'name': 'Name',
            'number': 'Phone',
            'email': 'E-mail',
            'message': 'Message'
        }


        
