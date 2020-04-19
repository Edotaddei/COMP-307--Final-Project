from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

app_name = 'listing'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new', views.product_create, name='new'),
    path('products/<pk>/update', ProductUpdate.as_view(), name='update'),
    path('products', ProductList.as_view(), name='list'),
    path('products/<pk>/', ProductDetail.as_view(), name='detail'),
    path('products/<pk>/trade', views.product_trade, name='trade'),
    path('cart', Cart.as_view(), name='cart'),
    path('products/<pk>/add', views.add_to_cart, name='add'),
    path('products/<pk>/delete', ProductDelete.as_view(), name='delete'),
    path('myproducts', myproducts.as_view(), name='myproducts'),
    path('products/<pk>/remove', views.remove_from_cart, name='remove'),

]