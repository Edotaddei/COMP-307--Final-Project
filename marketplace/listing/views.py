from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product,Order, OrderProduct
from .forms import ProductForm, ProductUpdateForm
from django.views.generic import (DetailView,
                                  ListView,
                                  TemplateView,
                                  CreateView)

from django.contrib.auth.decorators import login_required

@login_required
def ProductCreate(request):
    context = {}
    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)
        #form.photo = request.FILES['photo']
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner= request.user
            inst.save()
            return HttpResponseRedirect(reverse('listing:list'))
        context['form'] = form
    return render(request, 'listing/product_form.html',context)


def ProductTrade(request, **kwargs):
    primary_key = kwargs['pk']
    try:
        product = Product.objects.get(pk = primary_key)
        user = request.user
    except Product.DoesNotExist:
        raise HTTP404("Product does not exist")

    my_products = Product.objects.all().filter(owner=user)
    return render(request, 'listing/product_trade_form.html', context={'product':product, 'user':user, 'mine':my_products})

    
#class ProductCreate(CreateView):
 #   model = Product
  #  form_class = ProductForm
   # template_name = 'listing/product_form.html'
    #@method_decorator(login_required)
    #def get_success_url(self):
     #   messages.success(self.request, 'Product added to the marketplace!')
      #  return self.object.get_absolute_url()
       # #return HttpResponseRedirect(reverse('list'))

class ProductDetail(DetailView):
    model = Product
    template_name = 'listing/product_detail.html'
    

    def detail_view(request, primary_key, **kwargs):
      try:
        product = Product.objects.get(pk = primary_key)
      except Product.DoesNotExist:
        raise HTTP404("Product does not exist")
      return render(request, template_name, context={'product': product})


class ProductList(ListView):
    model = Product
    context_object_name = 'list'
    template_name = 'listing/product_list.html'

    def get_context_data(self, **kwargs):
      context = ListView.get_context_data(self,**kwargs)
      return context
    


#@login_required
class ProductUpdate(TemplateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'listing/product_update.html'
    @method_decorator(login_required)
    def get_success_url(self):
        messages.success(self.request, 'You have updated your product!')
        return self.object.get_absolute_url()

#@login_required
#def Cart(request):
 # return render(request,'listing/cart.html')

class Cart(ListView):
    model = Order
    context_object_name = 'list'
    template_name = 'listing/cart.html'

    def get_context_data(self, **kwargs):
      context = ListView.get_context_data(self,**kwargs)
      return context


def addtocart(request, **kwargs):
  primary_key = kwargs['pk']
  try:
    product = Product.objects.get(pk = primary_key)

  except Product.DoesNotExist:
        raise HTTP404("Product does not exist")

  order_product,created = OrderProduct.objects.get_or_create(product=product, owner_name=request.user.username, is_ordered=False)

  current_order = Order.objects.filter(owner=request.user, is_ordered=False)
  if current_order:
    order = current_order[0]
    #return HttpResponse('hello')
    if order.products.filter(product_id = primary_key).exists():
      order_product.count +=1
      order_product.save()
    else:
      order.products.add(order_product)
  else:
    order = Order.objects.create(owner=request.user,date=timezone.now())
    order.products.add(order_product)

  return HttpResponseRedirect(reverse('listing:list'))

