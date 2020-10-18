from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
from django.db.models import Q  #this Q is different from small q in the get queryset function


class SearchProductView(ListView):  #we get object_list name to pase through each object stored
    model = Product
    template_name = "search/view.html"
    
    def get_queryset(self,*args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(tag__title__icontains=query)  #lookup is a normal variable
            return Product.objects.filter(lookups).distinct()
        return Product.objects.none()
        
        '''
        __icontains = fields contains this, where i deals with all the captial and small letters  
        __iexact = field is exactly this, where i deals with all the captial and small letters

        '''

    
