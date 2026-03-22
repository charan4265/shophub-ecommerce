# core/views.py
# ─────────────────────────────────────────────
# Homepage view
# ─────────────────────────────────────────────

from django.shortcuts import render
from products.models import Product, Category
from sellers.models import Store


def homepage(request):
    """
    Main landing page — shows featured products,
    categories and active stores
    """
    # Latest 8 active products
    featured_products = Product.objects.filter(
        is_active=True,
        store__is_active=True
    ).order_by('-created_at')[:8]

    # All active categories
    categories = Category.objects.filter(is_active=True)

    # Active approved stores
    stores = Store.objects.filter(
        is_active=True, status='approved'
    ).order_by('-created_at')[:6]

    # Products on sale (have original_price set)
    deals = Product.objects.filter(
        is_active=True,
        store__is_active=True,
        original_price__isnull=False
    ).order_by('-created_at')[:4]

    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories':        categories,
        'stores':            stores,
        'deals':             deals,
    })