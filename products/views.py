from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from .models import Product, ProductFile
from analytics.mixins import ObjectViewedMixin
from django.views.generic import ListView, DetailView, View
from analytics.signals import object_viewed_signal
from carts.models import Cart
from django.contrib import messages

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


class UserProductHistoryView(LoginRequiredMixin, ListView):  #we get object_list name to pase through each object stored
    template_name = "products/user-history.html"

    def get_context_data(self, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(**kwargs)
        cart_obj,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_queryset(self):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
        return views 
    

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

from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.conf import settings
import os
from orders.models import ProductPurchase
        
class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        qs = Product.objects.filter(slug=slug)
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not Found !")
        download_obj = downloads_qs.first()
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if request.user.is_authenticated:
                user_ready = False

        purchased_product = None
        if download_obj.free :
            can_download = True
            user_ready = True
        else :
            purchased_product = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_product:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You Don't Have access to download this item")
            return redirect(download_obj.get_default_url())
        
        file_root = settings.PROTECTED_ROOT
        filepath = download_obj.file.path
        final_filepath = os.path.join(file_root, filepath)
        with open (final_filepath, 'rb') as f:
            wrapper = FileWrapper(f)
            mimetype = 'application/force-download'
            guessed_mimetype = guess_type(filepath)[0]
            if guessed_mimetype :
                mimetype = guessed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)
            response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
            response["X-SendFile"] = str(download_obj.name)
            return response
        return redirect(download_obj.get_default_url())

    