from .views import cart_home,cart_update,checkout_home,checkout_done_view

from django.conf.urls import url,include


urlpatterns = [
    url(r'^$',cart_home,name='home'),
    url(r'^update/$',cart_update,name='update'),
    url(r'^checkout/$',checkout_home,name='checkout'),
    url(r'^checkout/success/$',checkout_done_view,name='success'),
    
 ]
    
    