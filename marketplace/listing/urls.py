from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

app_name = 'listing'
urlpatterns = [
    path('new', views.ProductCreate, name='create'),
    path('edit', ProductUpdate.as_view(), name='update'),
    path('details', ProductDetail.as_view(), name='detail'),
    path('products', ProductList.as_view(), name='list'),

]