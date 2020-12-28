from django.conf.urls import url,include
from .views import OderListView, OderDetailView, VerifyOwnership

urlpatterns = [
    url(r'^$',OderListView.as_view(),name='list'),
    url(r'^endpoint/verify/ownership/$',VerifyOwnership.as_view(),name='verify-ownership'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$',OderDetailView.as_view(),name='detail'),
]
    
     