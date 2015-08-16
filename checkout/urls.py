#checkout/urls.py
from django.conf.urls import url
from checkout.views import PricedItemList

urlpatterns = [
    url('^$', PricedItemList.as_view(), name='priceditem_list')
]
