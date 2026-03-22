# sellers/models.py
# ─────────────────────────────────────────────
# Seller Store model — each seller has one store
# ─────────────────────────────────────────────

from django.db import models
from accounts.models import User


class Store(models.Model):
    """
    Every seller has one Store.
    Created after seller registers and completes setup.
    """

    class Status(models.TextChoices):
        PENDING  = 'pending',  'Pending Approval'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        SUSPENDED= 'suspended','Suspended'

    # ── Relationships ─────────────────────────
    seller = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='store',
        limit_choices_to={'role': 'seller'}
    )

    # ── Store Info ────────────────────────────
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    logo        = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    banner      = models.ImageField(upload_to='store_banners/', blank=True, null=True)

    # ── Contact ───────────────────────────────
    email   = models.EmailField(blank=True)
    phone   = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city    = models.CharField(max_length=50, blank=True)
    state   = models.CharField(max_length=50, blank=True)

    # ── Commission ────────────────────────────
    # Platform takes this % from each sale
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00
    )

    # ── Status ────────────────────────────────
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    is_active  = models.BooleanField(default=False)

    # ── Timestamps ────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Store'
        verbose_name_plural = 'Stores'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.seller.get_full_name()})'

    def get_total_products(self):
        # Products app not built yet — returns 0 safely
        try:
            return self.products.filter(is_active=True).count()
        except Exception:
            return 0

    def get_total_orders(self):
        # Orders app not built yet — returns 0 safely
        try:
            return self.orders.count()
        except Exception:
            return 0