from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def info(request):
	return render(request,'shop/shop.html')

@login_required
def account_info(request):
	return render(request,'shop/account_info.html')