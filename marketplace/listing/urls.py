from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

app_name = 'listing'
urlpatterns = [
    path('new', views.ProductCreate, name='new'),
    path('edit', ProductUpdate.as_view(), name='update'),
    path('products', ProductList.as_view(), name='list'),
    path('products/<pk>/', ProductDetail.as_view(), name='detail'),
    path('products/<pk>/trade', views.ProductTrade, name='trade'),
    path('cart',Cart.as_view(), name='cart'),
    path('products/<pk>/addtocart',views.addtocart, name='addtocart')

]