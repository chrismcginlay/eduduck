#checkout/urls.py
from django.conf.urls import url
from checkout.views import (
    PricedItemCreate,
    PricedItemList
)

urlpatterns = [
    url('^$', PricedItemList.as_view(), name='priceditem_list'),
    url('^create/$', PricedItemCreate.as_view(), name='priceditem_create'),
]
