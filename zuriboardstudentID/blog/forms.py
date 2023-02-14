from django import forms
from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        #fields = "__all__"
        fields = ( 'name', 'price', 'image')
        labels = {
            'name': 'Name',
            'price': 'Price',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input ', 'placeholder': 'Name'}),
            'price': forms.NumberInput(attrs={'class': 'input ', 'placeholder': 'Price'}),
            #'content': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Content'}),
        }
