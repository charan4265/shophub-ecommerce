# products/views.py
# ─────────────────────────────────────────────
# Product CRUD views for sellers
# ─────────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sellers.models import Store
from sellers.views import seller_required
from .models import Product, Category
from .forms import ProductForm


@seller_required
def product_add(request):
    """
    Seller adds a new product to their store
    """
    store = get_object_or_404(Store, seller=request.user)
    form  = ProductForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        product       = form.save(commit=False)
        product.store = store
        product.save()
        messages.success(request, f'"{product.name}" added successfully!')
        return redirect('products:seller_products')

    return render(request, 'products/product_form.html', {
        'form':  form,
        'title': 'Add New Product',
        'store': store,
    })


@seller_required
def product_edit(request, slug):
    """
    Seller edits an existing product
    """
    store   = get_object_or_404(Store, seller=request.user)
    product = get_object_or_404(Product, slug=slug, store=store)
    form    = ProductForm(
        request.POST  or None,
        request.FILES or None,
        instance=product
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'"{product.name}" updated!')
        return redirect('products:seller_products')

    return render(request, 'products/product_form.html', {
        'form':    form,
        'title':   f'Edit — {product.name}',
        'product': product,
        'store':   store,
    })


@seller_required
def product_delete(request, slug):
    """
    Seller deletes a product (POST only for safety)
    """
    store   = get_object_or_404(Store, seller=request.user)
    product = get_object_or_404(Product, slug=slug, store=store)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('products:seller_products')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })


@seller_required
def seller_product_list(request):
    """
    List of all products belonging to the logged-in seller
    """
    store    = get_object_or_404(Store, seller=request.user)
    products = Product.objects.filter(store=store).order_by('-created_at')

    return render(request, 'products/seller_product_list.html', {
        'products': products,
        'store':    store,
    })


# ── Public Views (visible to all buyers) ──────

def product_list(request):
    """
    Homepage product listing — all active products
    """
    products   = Product.objects.filter(is_active=True, store__is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Filter by category if selected
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/product_list.html', {
        'products':        products,
        'categories':      categories,
        'selected_category': category_slug,
        'query':           query,
    })


def product_detail(request, slug):
    """
    Single product detail page
    """
    product  = get_object_or_404(Product, slug=slug, is_active=True)
    related  = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    reviews  = product.reviews.all()

    # Check if logged-in user already reviewed
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product, buyer=request.user
        ).first()

    review_form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product':     product,
        'related':     related,
        'reviews':     reviews,
        'user_review': user_review,
        'review_form': review_form,
    })
    
from .forms import ProductForm, ReviewForm
from .models import Product, Category, Review


@login_required
def add_review(request, slug):
    """
    Buyer submits a review for a product.
    Only buyers who haven't reviewed yet can submit.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Sellers can't review their own products
    if request.user.is_seller and hasattr(request.user, 'store'):
        if product.store == request.user.store:
            messages.error(request, "You can't review your own product.")
            return redirect('products:detail', slug=slug)

    # Check if already reviewed
    existing = Review.objects.filter(
        product=product, buyer=request.user
    ).first()

    if existing:
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('products:detail', slug=slug)

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review         = form.save(commit=False)
        review.product = product
        review.buyer   = request.user
        review.save()
        messages.success(request, 'Thank you for your review!')
        return redirect('products:detail', slug=slug)

    return render(request, 'products/add_review.html', {
        'form':    form,
        'product': product,
    })


@login_required
def delete_review(request, review_id):
    """
    Buyer deletes their own review
    """
    review = get_object_or_404(Review, id=review_id, buyer=request.user)
    slug   = review.product.slug
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('products:detail', slug=slug)