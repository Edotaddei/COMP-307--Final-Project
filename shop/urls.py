from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.info, name='shop'),
    path('acc', views.account_info, name='account_info'),
    #path('login', views.do_login, name='login'),
    #path('logout', views.do_logout, name='logout'),
]
