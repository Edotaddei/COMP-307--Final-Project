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
'''
class CheckoutForm(forms.Form):
    street = forms.CharField(required=True)
    number = forms.CharField(required=True)
    city = forms.CharField(required=True)
    zip = forms.CharField(required=True)
    country = forms.CharField(required=True)
    '''






