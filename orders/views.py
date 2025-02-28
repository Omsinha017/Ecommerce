from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Order, ProductPurchase
from billing.models import BillingProfile
from django.http import Http404, JsonResponse

class OderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id = self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        return Http404
 
class LibrarayView(LoginRequiredMixin, ListView):
    template_name = 'orders/library.html'
    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax() :
            data = request.GET
            product_id = request.GET.get('product_id', None)
            if  product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner':True})
            return JsonResponse({'owner':False})
        raise Http404
