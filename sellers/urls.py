# sellers/urls.py

from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('setup/',                          views.store_setup,          name='setup'),
    path('dashboard/',                      views.seller_dashboard,     name='dashboard'),
    path('edit/',                           views.store_edit,           name='edit'),
    path('store/<slug:slug>/',              views.public_store,         name='public_store'),
    path('orders/',                         views.seller_orders,        name='orders'),
    path('orders/update/<int:order_id>/',   views.update_order_status,  name='update_order_status'),
]