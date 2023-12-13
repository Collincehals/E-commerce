from django import forms
from .models import *
from django.forms import ModelForm

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['seller','id','reviews']
        
        labels = {
            'tags': 'Category',
            'name': 'Product Name',
            'image': 'Product Photo',
            'description': 'Product Description',
            'stock': 'Product Quantity',
        }
        
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(),
            'description': forms.Textarea(attrs={'rows':3}),
            'specifications':forms.Textarea(attrs={'rows':3,'Placeholder':'Product Specifications...'}),
        }
        
        
   