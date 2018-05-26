from django.contrib import admin
from .models import *

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderStatus._meta.fields]

    class Meta:
        model = OrderStatus

admin.site.register(OrderStatus, OrderStatusAdmin)


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]
    inlines = [ProductInOrderInline]
    extra = 0

    class Meta:
        model = ProductInOrder

admin.site.register(ProductInOrder, ProductInOrderAdmin)
