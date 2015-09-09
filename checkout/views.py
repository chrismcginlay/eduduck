from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from checkout.models import Payment, PricedItem

class PricedItemList(ListView):
    model = PricedItem

class PricedItemCreate(CreateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']
    success_url = '/priced_items/'
    template_name_suffix = '_create_form'
    
    def form_valid(self, form):
        #mess around with form instance values here?
        #form.instance.currency=PricedItem.GBP
        return super(PricedItemCreate, self).form_valid(form)

class PricedItemUpdate(UpdateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']
    success_url = '/priced_items/' 
    template_name_suffix = '_update_form'

class PricedItemDelete(DeleteView):
    model = PricedItem
    success_url = '/priced_items/'

class PricedItemDetail(DetailView):
    model = PricedItem


class PaymentList(ListView):
    model = Payment

class PaymentList_forUser(ListView):
    def get_queryset(self):
        self.paying_user = get_object_or_404(User, id=self.request.user.id) 

    template_name = 'checkout/payment_for_user.html'
