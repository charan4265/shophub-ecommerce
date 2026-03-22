# products/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_active', 'created_at')
    list_filter   = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    """Show extra images inside product admin page"""
    model  = ProductImage
    extra  = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'store', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter   = ('is_active', 'condition', 'category')
    search_fields = ('name', 'store__name')
    readonly_fields = ('created_at', 'updated_at', 'slug')
    inlines       = [ProductImageInline]

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('product', 'buyer', 'rating', 'created_at')
    list_filter   = ('rating',)
    search_fields = ('product__name', 'buyer__email')