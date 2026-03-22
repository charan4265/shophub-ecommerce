# accounts/admin.py
# ─────────────────────────────────────────────
# Register User model in Django admin panel
# ─────────────────────────────────────────────

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin view for our User model
    """
    list_display  = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)

    fieldsets = (
        ('Login Info',   {'fields': ('email', 'password')}),
        ('Personal Info',{'fields': ('first_name', 'last_name', 'phone', 'avatar', 'address')}),
        ('Role',         {'fields': ('role',)}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')