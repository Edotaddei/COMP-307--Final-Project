from django.forms import ModelForm
from .models import Product, Address

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



class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['street',
                  'number',
                  'city',
                  'zip',
                  'country']







