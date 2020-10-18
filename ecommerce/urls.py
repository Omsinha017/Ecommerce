"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.generic import TemplateView
from accounts.views import LoginView,guest_register_view,RegisterView
from django.contrib.auth.views import LogoutView
from billing.views import payment_method_view, payment_method_createview
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home_page,name='home'),
    url(r'^contact/$',views.Contact_page,name="contact"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^register/guest/$',guest_register_view,name="guest_register"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^api/cart/$',cart_detail_api_view,name="api-cart"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^billing/payment-method/$',payment_method_view,name="billing-payment-method"),
    url(r'^billing/payment-method/create/$',payment_method_createview,name="billing-payment-method-endpoint"),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    url(r'^bootstrap/$',TemplateView.as_view(template_name="bootstrap/example.html")),
    url(r'^products/',include(("products.urls",'products'),namespace="products")),
    url(r'^search/',include(("search.urls",'search'),namespace="search")),
    url(r'^settings/email/$',MarketingPreferenceUpdateView.as_view(), name="marketing-pref"),
    url(r'^webhooks/mailchimp/$',MailchimpWebhookView.as_view(), name="webhooks-mailchimp"),
    url(r'^cart/',include(("carts.urls",'carts'),namespace="cart")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)