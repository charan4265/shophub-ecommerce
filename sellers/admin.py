# sellers/admin.py
# ─────────────────────────────────────────────
# Admin panel config for Store model
# ─────────────────────────────────────────────

from django.contrib import admin
from django.utils.html import format_html
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display  = ('name', 'seller', 'status', 'is_active', 'commission_rate', 'created_at', 'approve_button')
    list_filter   = ('status', 'is_active')
    search_fields = ('name', 'seller__email', 'seller__first_name')
    readonly_fields = ('created_at', 'updated_at')

    actions = ['approve_stores', 'reject_stores']

    def approve_button(self, obj):
        if obj.status == Store.Status.PENDING:
            return format_html(
                '<a class="button" href="/admin/sellers/store/{}/change/">Review</a>', obj.pk
            )
        return obj.get_status_display()
    approve_button.short_description = 'Action'

    def approve_stores(self, request, queryset):
        queryset.update(status=Store.Status.APPROVED, is_active=True)
        self.message_user(request, f'{queryset.count()} store(s) approved.')
    approve_stores.short_description = 'Approve selected stores'

    def reject_stores(self, request, queryset):
        queryset.update(status=Store.Status.REJECTED, is_active=False)
        self.message_user(request, f'{queryset.count()} store(s) rejected.')
    reject_stores.short_description = 'Reject selected stores'