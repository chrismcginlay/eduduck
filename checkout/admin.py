from django.contrib import admin

from checkout.models import Payment, PricedItem

admin.site.register(Payment)
admin.site.register(PricedItem)
