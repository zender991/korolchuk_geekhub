from django.contrib import admin

from product.models import (Category,
                            Subcategory,
                            Product,
                            Order,
                            Currency)


class OrdersAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'order_details', 'subtotal']
    list_display = ('name', 'email', 'subtotal')


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Currency)