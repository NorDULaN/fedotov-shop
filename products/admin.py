from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

    class Meta:
        model = Category

admin.site.register(Category , MPTTModelAdmin)

# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = (
        'available',
        'created',
        'updated',
        ('category', TreeRelatedFieldListFilter),
    )
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ProductImageInline]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)
