from django.contrib import admin
#
from .models import Product
from .models import Order


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'price', 'quantity'
    )


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'shop', 'client', 'status', 'date_add','created_at')


admin.site.register(Order, OrderAdmin)
