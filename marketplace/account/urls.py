from django.urls import path, include

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.info, name='account_info'),
    path('signup', views.signup, name='signup'),
    path('login', views.do_login, name='login'),
    path('logout', views.do_logout, name='logout')
]
