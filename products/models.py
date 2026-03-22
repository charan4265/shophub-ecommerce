# products/models.py
# ─────────────────────────────────────────────
# Category and Product models
# ─────────────────────────────────────────────

from django.db import models
from django.utils.text import slugify
from sellers.models import Store


class Category(models.Model):
    """
    Product categories e.g. Electronics, Clothing, Books
    Created by Admin in the admin panel
    """
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering            = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    A product listed by a seller in their store
    """

    class Condition(models.TextChoices):
        NEW        = 'new',        'New'
        USED       = 'used',       'Used'
        REFURBISHED= 'refurbished','Refurbished'

    # ── Relationships ─────────────────────────
    store    = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='products'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )

    # ── Basic Info ────────────────────────────
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    condition   = models.CharField(
        max_length=15, choices=Condition.choices, default=Condition.NEW
    )

    # ── Pricing ───────────────────────────────
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    original_price= models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Original price before discount (optional)'
    )

    # ── Stock ─────────────────────────────────
    stock     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # ── Main Image ────────────────────────────
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # ── Timestamps ────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.store.name}'

    def save(self, *args, **kwargs):
        # Auto-generate unique slug from product name
        if not self.slug:
            base_slug = slugify(self.name)
            slug      = base_slug
            counter   = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        """Calculate % discount if original price is set"""
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return None
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()


class ProductImage(models.Model):
    """
    Extra images for a product (up to 4 additional images)
    """
    product    = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image      = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.product.name}'

class Review(models.Model):
    """
    A buyer's review on a product.
    One review per buyer per product.
    """
    product  = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    buyer    = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='reviews'
    )
    rating   = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]  # 1 to 5 stars
    )
    title    = models.CharField(max_length=100, blank=True)
    comment  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One review per buyer per product
        unique_together = ('product', 'buyer')
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.rating}★ by {self.buyer.get_full_name()} on {self.product.name}'