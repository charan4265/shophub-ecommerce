# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import homepage

urlpatterns = [
    path('',          homepage, name='home'),
    path('admin/',    admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('sellers/',  include('sellers.urls',  namespace='sellers')),
    path('products/', include('products.urls', namespace='products')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('',          include('orders.urls',   namespace='orders')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
