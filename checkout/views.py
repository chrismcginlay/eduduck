from django.shortcuts import render
from django.views.generic import ListView
from checkout.models import PricedItem

class PricedItemList(ListView):
    model = PricedItem
