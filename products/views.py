from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Product
from analytics.mixins import ObjectViewedMixin
from django.views.generic import ListView,DetailView
from analytics.signals import object_viewed_signal
from carts.models import Cart

# Create your views here.

class ProductListView(ListView):  #we get object_list name to pase through each object stored
    model = Product
    template_name = "products/list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        request = self.request
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    model = Product
    template_name = "products/detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context
    
    def get_object(self,*args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not Found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
        except:
            raise Http404("Uhmmm ")

        object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance

    
