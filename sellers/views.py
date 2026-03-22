# sellers/views.py
# ─────────────────────────────────────────────
# Views for seller store setup and dashboard
# ─────────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Store
from .forms import StoreSetupForm, StoreEditForm


def seller_required(view_func):
    """
    Decorator — only allows sellers to access a view.
    Redirects others to homepage.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_seller:
            messages.error(request, 'You need a seller account to access this page.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


@seller_required
def store_setup(request):
    """
    First-time store setup page shown right after seller registers.
    If seller already has a store, redirect to dashboard.
    """
    # If store already exists, skip setup
    if hasattr(request.user, 'store'):
        return redirect('sellers:dashboard')

    form = StoreSetupForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        store = form.save(commit=False)
        store.seller = request.user

        # Auto-generate a unique slug from store name
        base_slug = slugify(store.name)
        slug      = base_slug
        counter   = 1
        while Store.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        store.slug = slug

        store.save()
        messages.success(
            request,
            'Store created! Our team will review and approve it shortly.'
        )
        return redirect('sellers:dashboard')

    return render(request, 'sellers/store_setup.html', {'form': form})


@seller_required
def seller_dashboard(request):
    """
    Main seller dashboard — shows store stats and recent orders
    """
    store = getattr(request.user, 'store', None)

    if not store:
        return redirect('sellers:setup')

    # Get recent order items for this store
    from orders.models import OrderItem
    recent_order_items = OrderItem.objects.filter(
        store=store
    ).select_related('order').order_by('-order__created_at')[:5]

    # Count pending orders
    pending_orders = OrderItem.objects.filter(
        store=store,
        order__status='pending'
    ).count()

    # Calculate total revenue
    from django.db.models import Sum
    from decimal import Decimal
    revenue_data = OrderItem.objects.filter(
        store=store,
        order__payment_status__in=['paid', 'cod']
    ).aggregate(total=Sum('price_at_purchase'))
    total_revenue = revenue_data['total'] or Decimal('0')

    context = {
        'store':              store,
        'total_products':     store.get_total_products(),
        'pending_orders':     pending_orders,
        'total_revenue':      total_revenue,
        'recent_order_items': recent_order_items,
        'status':             store.get_status_display(),
    }
    return render(request, 'sellers/dashboard.html', context)
@seller_required
def store_edit(request):
    """
    Edit store details
    """
    store = get_object_or_404(Store, seller=request.user)
    form  = StoreEditForm(
        request.POST  or None,
        request.FILES or None,
        instance=store
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Store updated successfully!')
        return redirect('sellers:dashboard')

    return render(request, 'sellers/store_edit.html', {'form': form, 'store': store})


def public_store(request, slug):
    """
    Public-facing store page — visible to all buyers
    """
    store    = get_object_or_404(Store, slug=slug, is_active=True)
    products = store.products.filter(is_active=True)

    return render(request, 'sellers/public_store.html', {
        'store':    store,
        'products': products,
    })
    
# ── Add these at the bottom of sellers/views.py ──

from orders.models import Order, OrderItem


@seller_required
def seller_orders(request):
    """
    All orders containing products from this seller's store
    """
    store  = get_object_or_404(Store, seller=request.user)
    # Get all order items belonging to this seller's store
    order_items = OrderItem.objects.filter(
        store=store
    ).select_related('order', 'product').order_by('-order__created_at')

    return render(request, 'sellers/seller_orders.html', {
        'order_items': order_items,
        'store':       store,
    })


@seller_required
def update_order_status(request, order_id):
    """
    Seller updates the status of an order item
    e.g. Confirmed → Processing → Shipped → Delivered
    """
    store      = get_object_or_404(Store, seller=request.user)
    order_item = get_object_or_404(OrderItem, id=order_id, store=store)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order      = order_item.order

        # Update the parent order status
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()

            # Send email notification to buyer
            send_order_status_email(order, new_status)

            messages.success(
                request,
                f'Order #{order.order_number} status updated to {order.get_status_display()}.'
            )

    return redirect('sellers:orders')


def send_order_status_email(order, status):
    """
    Sends an email to buyer when order status changes.
    In development this prints to terminal instead of sending real email.
    """
    from django.core.mail import send_mail
    from django.conf import settings

    status_messages = {
        'confirmed':  'Your order has been confirmed by the seller!',
        'processing': 'Your order is being processed and packed.',
        'shipped':    'Great news! Your order has been shipped and is on its way.',
        'delivered':  'Your order has been delivered. Enjoy your purchase!',
        'cancelled':  'Unfortunately your order has been cancelled.',
    }

    message = status_messages.get(status, 'Your order status has been updated.')

    try:
        send_mail(
            subject=f'Order #{order.order_number} — {order.get_status_display()}',
            message=f'''
Hi {order.full_name},

{message}

Order Details:
- Order #: {order.order_number}
- Status: {order.get_status_display()}
- Total: ₹{order.total_amount}

Thank you for shopping with ShopHub!
            ''',
            from_email='noreply@shophub.com',
            recipient_list=[order.email],
            fail_silently=True,
        )
    except Exception:
        pass  # Don't crash if email fails