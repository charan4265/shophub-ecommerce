# orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/',                           views.cart_view,      name='cart'),
    path('cart/add/<int:product_id>/',      views.add_to_cart,    name='add_to_cart'),
    path('cart/remove/<int:item_id>/',      views.remove_from_cart,name='remove_from_cart'),
    path('cart/update/<int:item_id>/',      views.update_cart,    name='update_cart'),
    path('checkout/',                       views.checkout,       name='checkout'),
    path('orders/',                         views.order_list,     name='order_list'),
    path('orders/<str:order_number>/',      views.order_detail,   name='order_detail'),
]