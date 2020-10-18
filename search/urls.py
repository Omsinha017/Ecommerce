from .views import SearchProductView
from django.conf.urls import url,include


urlpatterns = [
    url(r'^$',SearchProductView.as_view(),name='query'),
 ]
    
    