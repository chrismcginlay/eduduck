from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from checkout.models import PricedItem

class PricedItemList(ListView):
    model = PricedItem

class PricedItemCreate(CreateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']
    success_url = '/priced_items/'
    
    def form_valid(self, form):
        #mess around with form instance values here?
        #form.instance.currency=PricedItem.GBP
        return super(PricedItemCreate, self).form_valid(form)

class PricedItemUpdate(UpdateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']

class PricedItemDelete(DeleteView):
    model = PricedItem

class PricedItemDetail(DetailView):
    model = PricedItem
