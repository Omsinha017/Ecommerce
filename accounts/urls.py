from django.conf.urls import url,include
from products.views import UserProductHistoryView
from .views import AccountHomeView, AccountEmailActivationView,UserDetailUpdateView

urlpatterns = [
    url(r'^$',AccountHomeView.as_view(),name='home'),
    url(r'history/product/$',UserProductHistoryView.as_view(),name='user-product-history'),
    url(r'^details/$',UserDetailUpdateView.as_view(),name='user-update'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',AccountEmailActivationView.as_view(),name='email-activate'),
    url(r'^email/resend-activtion/$',AccountEmailActivationView.as_view(),name='resend-activtion'),
]
    
    