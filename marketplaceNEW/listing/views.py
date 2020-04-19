from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Product, Order, OrderProduct
from .forms import ProductForm, ProductUpdateForm
from django.views.generic import (DetailView,
                                  ListView,
                                  TemplateView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from django.contrib.auth.decorators import login_required


@login_required
def product_create(request):
    context = {}
    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)
        # form.photo = request.FILES['photo']
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            return HttpResponseRedirect(reverse('listing:list'))
        context['form'] = form
    return render(request, 'listing/product_form.html', context)


def product_trade(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        product = Product.objects.get(pk=primary_key)
        user = request.user
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    my_products = Product.objects.all().filter(owner=user)
    return render(request, 'listing/product_trade_form.html',
                  context={'product': product, 'user': user, 'mine': my_products})


class ProductDetail(DetailView):
    model = Product
    template_name = 'listing/product_detail.html'


class HomeView(TemplateView):
    model = Product
    template_name = 'listing/home.html'


class ProductList(ListView):
    model = Product
    context_object_name = 'list'
    template_name = 'listing/product_list.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context


class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'image', 'description', 'price', 'count', 'category']
    template_name_suffix = '_form_update'
    success_url = "/listing/products"


class ProductDelete(DeleteView):
    model = Product
    success_url = "/listing/products"


class Cart(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'listing/cart.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context


def add_to_cart(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        product = Product.objects.get(pk=primary_key)

    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    if product.count < 1:
        return HttpResponse("Product no longer in stock")
    else:
        product.count -= 1
        product.save()

    order_product, created = OrderProduct.objects.get_or_create(product=product, is_ordered=False)
    try:
        order = Order.objects.get(owner=request.user, is_ordered=False)
    except Order.DoesNotExist:
        order = Order.objects.create(owner=request.user, date=timezone.now())
        order.products.add(order_product)
        order.save()
        return HttpResponseRedirect(reverse('listing:list'))
    if order.products.filter(product_id=primary_key).exists():
        order_product.count += 1
        order_product.save()
    else:
        order.products.add(order_product)
        order.save()

    return HttpResponseRedirect(reverse('listing:list'))


def remove_from_cart(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        order_product = OrderProduct.objects.get(pk=primary_key)
    except OrderProduct.DoesNotExist:
        raise Http404("OrderProduct does not exist")
    order_product.count -= 1
    if order_product.count == 0:
        order_product.delete()
    else:
        order_product.save()

    try:
        product = Product.objects.get(name=order_product.product)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    product.count += 1
    product.save()

    current_order = Order.objects.get(owner=request.user, is_ordered=False)
    if not current_order.products.exists():
        current_order.delete()
    return HttpResponseRedirect(reverse('listing:cart'))


class myproducts(ListView):
    model = Product
    context_object_name = 'list'
    template_name = 'listing/my_product_list.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context
