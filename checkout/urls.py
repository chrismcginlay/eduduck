#checkout/urls.py
from django.conf.urls import url
from checkout.views import (
    PaymentList,
    PricedItemCreate,
    PricedItemDetail,
    PricedItemDelete, 
    PricedItemList,
    PricedItemUpdate,
)

urlpatterns = [
    url(r'^$', PricedItemList.as_view(), name='priceditem_list'),
    url(
        r'^create/$',
        PricedItemCreate.as_view(),
        name='priceditem_create'
    ),
    url(
        r'^(?P<pk>\d+)/$', 
        PricedItemDetail.as_view(), 
        name='priceditem_detail'
    ),
    url(
        r'^(?P<pk>\d+)/delete/$', 
        PricedItemDelete.as_view(), 
        name='priceditem_delete'
    ),
    url(
        r'^(?P<pk>\d+)/update/$', 
        PricedItemUpdate.as_view(), 
        name='priceditem_update'
    ),

    url(
        r'^payment/$',
        PaymentList.as_view(),
        name='payment_list'
    ),
    url(
        r'^payment/user/(?P<pk>\d+)/$',
        PaymentList.as_view(),
        name='payment_list_for_user'
    ),
    url(
        r'^payment/object_type/(?P<content_type_id>\d+)/object/(?P<pk>\d+)$',
        PaymentList.as_view(),
        name='payment_list_for_object'
    ), 
]
