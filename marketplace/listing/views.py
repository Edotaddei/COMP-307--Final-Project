from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Product, Order, OrderProduct, Address, TradeProduct, TradeRequest
from .forms import ProductForm, ProductUpdateForm, AddressForm
from django.views.generic import (DetailView,
                                  ListView,
                                  TemplateView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from django.contrib.auth.decorators import login_required
import chat


@login_required
def product_create(request):
    context = {}
    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            return HttpResponseRedirect(reverse('listing:list'))
        context['form'] = form
    return render(request, 'listing/product_form.html', context)


@login_required
def product_trade(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        product = Product.objects.get(pk=primary_key)
        user = request.user
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    my_products = Product.objects.all().filter(owner=user)

    if request.method == 'POST':
        #check if the products are in stock
        product_client = Product.objects.get(pk=request.POST.get('prova'))
        if product.count < 1 or product_client.count < 1:
            return HttpResponse('The product you are trying to trade is out of stock')

        trade_request = TradeRequest.objects.create(requester=request.user)
        trade_product_client = TradeProduct.objects.create(product=product_client)
        trade_product_seller = TradeProduct.objects.create(product=product)
        trade_request.products.add(trade_product_client)
        trade_request.products.add(trade_product_seller)
        
        trade_request.receiver_username = product.owner.username
        trade_request.save()

        if request.POST.get('wantMsg'):
            return HttpResponseRedirect(reverse('chat:room', args={product.owner.username}))
        else:
            return HttpResponseRedirect(reverse('listing:list'))
        
    return render(request, 'listing/product_trade_form.html',
                  context={'product': product, 'user': user, 'mine': my_products})


@login_required
def trade_decision(request, **kwargs):
    primary_key = kwargs['pk']
    context = {}

    if request.method == 'POST':
        try:
            trade = TradeRequest.objects.get(pk=primary_key)
        except Product.DoesNotExist:
            raise Http404("Trade does not exist")

        trade.is_concluded = True
        #if the trade has been accepted, reduce the product counts by 1
        if request.POST['trade_decision'] == 'yes':
            trade.is_accepted = True

            for tp in trade.products.all():
                tp.product.count -=1
                tp.product.save()

        else:
            trade.is_rejected = True

        trade.save()
        return HttpResponseRedirect(reverse('listing:list'))

    return render(request, 'listing/trade_decision.html')


class TradeList(ListView):
    model = TradeRequest
    context_object_name = 'list'
    template_name = 'listing/trade_list.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        
        return context
        

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


@login_required
def ProductDelete(self, **kwargs):
    primary_key= kwargs['pk']
    try:
        product = Product.objects.get(pk=primary_key)

    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    product.is_deleted = True
    product.save()
    return HttpResponseRedirect(reverse('listing:list'))


class Cart(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'listing/cart.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context


@login_required
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
    
    #if a user has a running order, use that, otherwise create a new order
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


@login_required
def remove_from_cart(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        order_product = OrderProduct.objects.get(pk=primary_key)
    except OrderProduct.DoesNotExist:
        raise Http404("OrderProduct does not exist")

    try:
        product = Product.objects.get(name=order_product.product)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    product.count += 1
    product.save()

    order_product.count -= 1
    if order_product.count == 0:
        order_product.delete()
    else:
        order_product.save()

    current_order = Order.objects.get(owner=request.user, is_ordered=False)
    if not current_order.products.exists():
        current_order.delete()
    return HttpResponseRedirect(reverse('listing:cart'))


class MyProducts(ListView):
    model = Product
    context_object_name = 'list'
    template_name = 'listing/my_product_list.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context

@login_required
def checkout(request, **kwargs):

    primary_key = kwargs['pk']
    try:
        order = Order.objects.get(pk=primary_key)
    except Order.DoesNotExist:
        raise Http404("OrderProduct does not exist")

    context = {}

    if request.method == 'POST':
        form = AddressForm(request.POST)
        
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.order = order
            inst.save()
            order.is_ordered=True
            order.date = timezone.now()
            order.save()
            #op = order product
            for op in order.products.all():
                op.is_ordered = True
                op.save()

            return HttpResponseRedirect(reverse('listing:list'))
        context['form'] = form
    
    return render(request, 'listing/checkout.html', context={'order':order})


class MyOrders(ListView):
    model = Order
    context_object_name = 'list'
    template_name = 'listing/my_order_list.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context


class OrderDetails(TemplateView):
    model = Order
    template_name = 'listing/order_details.html'

    def get_context_data(self, **kwargs):
        context={}
        primary_key = kwargs['pk']
        try:
            order = Order.objects.get(pk=primary_key)
        except Order.DoesNotExist:
            raise Http404("OrderProduct does not exist")

        try:
            address = Address.objects.get(order=order)
        except Address.DoesNotExist:
            raise Http404("Address does not exist")
            
        context['order']=order
        context['address']=address
        return context