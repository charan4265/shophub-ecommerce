# accounts/models.py
# ─────────────────────────────────────────────
# Custom User Model — supports Buyer, Seller, Admin roles
# ─────────────────────────────────────────────

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager to create users using email instead of username
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model — uses email to login instead of username.
    Every user has one of three roles: Buyer, Seller, or Admin.
    """

    class Role(models.TextChoices):
        BUYER  = 'buyer',  'Buyer'
        SELLER = 'seller', 'Seller'
        ADMIN  = 'admin',  'Admin'

    # ── Core fields ───────────────────────────
    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    role       = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    # ── Profile ───────────────────────────────
    phone    = models.CharField(max_length=15, blank=True)
    avatar   = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address  = models.TextField(blank=True)

    # ── Status flags ──────────────────────────
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # Login with email, not username
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name      = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    # ── Helper properties ─────────────────────
    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN