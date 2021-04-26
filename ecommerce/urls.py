from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from accounts.views import LoginView,GuestRegisterView,RegisterView
from django.contrib.auth.views import LogoutView
from billing.views import payment_method_view, payment_method_createview
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibrarayView
from analytics.views import SalesView, SalesAjaxView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home_page,name='home'),
    url(r'^accounts/$',RedirectView.as_view(url='/account')),
    url(r'^account/',include(("accounts.urls",'accounts'),namespace="account")),
    url(r'^orders/',include(("orders.urls",'orders'),namespace="orders")),
    url(r'^accounts/',include("accounts.passwords.urls")),
    url(r'^analytics/sales/$',SalesView.as_view(),name="sales-analytics"),
    url(r'^analytics/sales/data/$',SalesAjaxView.as_view(),name="sales-analytics-data"),
    url(r'^contact/$',views.Contact_page,name="contact"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^register/guest/$',GuestRegisterView.as_view(),name="guest_register"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^api/cart/$',cart_detail_api_view,name="api-cart"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^billing/payment-method/$',payment_method_view,name="billing-payment-method"),
    url(r'^billing/payment-method/create/$',payment_method_createview,name="billing-payment-method-endpoint"),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    url(r'library/$', LibrarayView.as_view(), name ='library'),
    url(r'^bootstrap/$',TemplateView.as_view(template_name="bootstrap/example.html")),
    url(r'^products/',include(("products.urls",'products'),namespace="products")),
    url(r'^search/',include(("search.urls",'search'),namespace="search")),
    url(r'^settings/$',RedirectView.as_view(url='/account')),
    url(r'^settings/email/$',MarketingPreferenceUpdateView.as_view(), name="marketing-pref"),
    url(r'^webhooks/mailchimp/$',MailchimpWebhookView.as_view(), name="webhooks-mailchimp"),
    url(r'^cart/',include(("carts.urls",'carts'),namespace="cart")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)