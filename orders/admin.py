# orders/admin.py

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model         = OrderItem
    extra         = 0
    readonly_fields = ('product', 'store', 'quantity', 'price_at_purchase', 'product_name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('order_number', 'buyer', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter     = ('status', 'payment_status')
    search_fields   = ('order_number', 'buyer__email', 'full_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines         = [OrderItemInline]