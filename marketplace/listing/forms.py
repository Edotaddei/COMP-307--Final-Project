from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'image',
                  'description',
                  'price',
                  'count',
                  'category']
    

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'image',
                  'description',
                  'price',
                  'count',
                  'category']

class ProductTradeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'image',
                  'description',
                  'price',
                  'count',
                  'category']



