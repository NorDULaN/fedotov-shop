from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from .models import Category, Product
# Register your models here.

# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = (
        'available',
        'created',
        'updated',
        ('category', TreeRelatedFieldListFilter),
    )
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category , MPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
