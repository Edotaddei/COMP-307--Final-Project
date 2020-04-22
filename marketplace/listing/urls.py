from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views

app_name = 'listing'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new', views.product_create, name='new'),
    path('products', ProductList.as_view(), name='list'),
    path('products/<pk>/', ProductDetail.as_view(), name='detail'),
    path('products/<pk>/update', login_required(ProductUpdate.as_view()), name='update'),
    path('products/<pk>/delete', views.ProductDelete, name='delete'),
    path('products/<pk>/trade', views.product_trade, name='trade'),
    path('products/<pk>/add', views.add_to_cart, name='add'),
    path('products/<pk>/remove', views.remove_from_cart, name='remove'),
    path('cart',login_required(Cart.as_view()), name='cart'),
    path('cart/<pk>/checkout',views.checkout,name='checkout'),
    path('myproducts', login_required(MyProducts.as_view()), name='myproducts'),
    path('myorders',login_required(MyOrders.as_view()),name='myorders'),
    path('myorders/<pk>/details', login_required(OrderDetails.as_view()),name='orderdetails'),
    path('mytrades',login_required(TradeList.as_view()),name = 'mytrades'),
    path('mytrades/<pk>/decision', views.trade_decision, name= 'tradedecision')
]