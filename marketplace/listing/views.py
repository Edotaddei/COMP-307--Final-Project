from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.views.generic import (DetailView,
                                  ListView,
                                  TemplateView,
                                  CreateView)

from django.contrib.auth.decorators import login_required

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


class ProductList(ListView):
    model = Product
    template_name = 'listing/product_list.html'

#@login_required
class ProductUpdate(TemplateView): #might have to use something other than template view not sure if its the right one
    model = Product
    form_class = ProductUpdateForm
    template_name = 'listing/product_update.html'
    @method_decorator(login_required)
    def get_success_url(self):
        messages.success(self.request, 'You have updated your product!')
        return self.object.get_absolute_url()
