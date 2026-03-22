# orders/views.py
# ─────────────────────────────────────────────
# Cart and Order views
# ─────────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


def get_or_create_cart(user):
    """Helper — gets existing cart or creates a new one"""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart.
    If already in cart, increase quantity.
    """
    product  = get_object_or_404(Product, id=product_id, is_active=True)
    cart     = get_or_create_cart(request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Check stock
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} units available.')
        return redirect('products:detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product
    )

    if not created:
        # Product already in cart — increase quantity
        new_qty = cart_item.quantity + quantity
        if new_qty > product.stock:
            messages.error(request, f'Only {product.stock} units available.')
            return redirect('products:detail', slug=product.slug)
        cart_item.quantity = new_qty
        cart_item.save()
        messages.success(request, f'Cart updated — {product.name} qty: {new_qty}')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'"{product.name}" added to cart!')

    return redirect('orders:cart')


@login_required
def cart_view(request):
    """
    Show the cart page with all items
    """
    cart = get_or_create_cart(request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def remove_from_cart(request, item_id):
    """
    Remove a single item from the cart
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    name      = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'"{name}" removed from cart.')
    return redirect('orders:cart')


@login_required
def update_cart(request, item_id):
    """
    Update quantity of a cart item
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity  = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    elif quantity > cart_item.product.stock:
        messages.error(request, f'Only {cart_item.product.stock} units available.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('orders:cart')


@login_required
def checkout(request):
    """
    Checkout page — shows address form and order summary.
    On submit, creates the order and clears the cart.
    """
    cart = get_or_create_cart(request.user)

    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')

    # Pre-fill form with user's saved info
    initial = {
        'full_name': request.user.get_full_name(),
        'email':     request.user.email,
        'phone':     request.user.phone,
    }
    form = CheckoutForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        # Create the Order
        order = Order.objects.create(
            buyer         = request.user,
            full_name     = form.cleaned_data['full_name'],
            email         = form.cleaned_data['email'],
            phone         = form.cleaned_data['phone'],
            address       = form.cleaned_data['address'],
            city          = form.cleaned_data['city'],
            state         = form.cleaned_data['state'],
            pincode       = form.cleaned_data['pincode'],
            total_amount  = cart.total_price,
        )

        # Create OrderItems from CartItems
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order             = order,
                product           = cart_item.product,
                store             = cart_item.product.store,
                quantity          = cart_item.quantity,
                price_at_purchase = cart_item.product.price,
                product_name      = cart_item.product.name,
            )
            # Reduce stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        # Clear the cart
        cart.items.all().delete()

        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('orders:order_detail', order_number=order.order_number)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
    })


@login_required
def order_detail(request, order_number):
    """
    Order confirmation and detail page
    """
    order = get_object_or_404(
        Order, order_number=order_number, buyer=request.user
    )
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    """
    Buyer's order history
    """
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})