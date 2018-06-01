from django.contrib import admin
from .models import *


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'customer_phone',
    'customer_comment', 'status', 'total_price', 'created']
    inlines = [ProductInOrderInline]
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

    class Meta:
        model = ProductInOrder

admin.site.register(ProductInOrder, ProductInOrderAdmin)


class ProductInCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInCart._meta.fields]

    class Meta:
        model = ProductInCart

admin.site.register(ProductInCart, ProductInCartAdmin)
