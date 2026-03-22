# orders/models.py
# ─────────────────────────────────────────────
# Cart, Order and OrderItem models
# ─────────────────────────────────────────────

from django.db import models
from accounts.models import User
from products.models import Product
from sellers.models import Store


class Cart(models.Model):
    """
    A cart belongs to one user.
    Created automatically when user adds first item.
    """
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart of {self.user.get_full_name()}'

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """
    One product line inside a cart
    """
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """
    A confirmed order placed by a buyer.
    One order can have items from multiple sellers.
    """
    class Status(models.TextChoices):
        PENDING    = 'pending',    'Pending'
        CONFIRMED  = 'confirmed',  'Confirmed'
        PROCESSING = 'processing', 'Processing'
        SHIPPED    = 'shipped',    'Shipped'
        DELIVERED  = 'delivered',  'Delivered'
        CANCELLED  = 'cancelled',  'Cancelled'
        REFUNDED   = 'refunded',   'Refunded'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        PAID   = 'paid',   'Paid'
        COD    = 'cod',    'Cash on Delivery'
        FAILED = 'failed', 'Failed'

    # ── Relationships ─────────────────────────
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name='orders'
    )

    # ── Unique order number ───────────────────
    order_number = models.CharField(max_length=20, unique=True, blank=True)

    # ── Delivery Address ──────────────────────
    full_name    = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=15)
    address      = models.TextField()
    city         = models.CharField(max_length=50)
    state        = models.CharField(max_length=50)
    pincode      = models.CharField(max_length=10)

    # ── Pricing ───────────────────────────────
    total_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ── Status ────────────────────────────────
    status         = models.CharField(max_length=15, choices=Status.choices,        default=Status.PENDING)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)

    # ── Timestamps ────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.order_number} by {self.buyer}'

    def save(self, *args, **kwargs):
        # Auto-generate order number like ORD-20240322-0001
        if not self.order_number:
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            rand_str = str(random.randint(1000, 9999))
            self.order_number = f'ORD-{date_str}-{rand_str}'
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    One product line inside an order.
    We store price at time of purchase so it
    doesn't change if seller edits the product later.
    """
    order    = models.ForeignKey(Order,   on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    store    = models.ForeignKey(Store,   on_delete=models.SET_NULL, null=True, related_name='orders')
    quantity = models.PositiveIntegerField()

    # Snapshot prices at time of purchase
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    product_name      = models.CharField(max_length=200)  # in case product is deleted

    def __str__(self):
        return f'{self.quantity} x {self.product_name}'

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity