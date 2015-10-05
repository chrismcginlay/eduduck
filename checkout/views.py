from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from checkout.models import Payment, PricedItem

class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(
        lambda u: u.is_superuser, 
        login_url='/', 
        redirect_field_name=None
    ))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)

class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class PricedItemList(SuperuserRequiredMixin, ListView):
    model = PricedItem

class PricedItemCreate(SuperuserRequiredMixin, CreateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']
    success_url = '/priced_items/'
    template_name_suffix = '_create_form'
    
    def form_valid(self, form):
        #mess around with form instance values here?
        #form.instance.currency=PricedItem.GBP
        return super(PricedItemCreate, self).form_valid(form)

class PricedItemUpdate(SuperuserRequiredMixin, UpdateView):
    model = PricedItem
    fields = ['content_type', 'object_id', 'fee_value', 'currency', 'tax_rate', 'notes']
    success_url = '/priced_items/' 
    template_name_suffix = '_update_form'

class PricedItemDelete(SuperuserRequiredMixin, DeleteView):
    model = PricedItem
    success_url = '/priced_items/'

class PricedItemDetail(LoginRequiredMixin, DetailView):
    model = PricedItem

class PaymentList(SuperuserRequiredMixin, ListView):
    model = Payment

class PaymentList_forUser(LoginRequiredMixin, ListView):
    def get_queryset(self):
        self.paying_user = get_object_or_404(User, id=self.request.user.id) 

    template_name = 'checkout/payment_for_user.html'

class PaymentDetail(LoginRequiredMixin, DetailView):
    model = Payment
