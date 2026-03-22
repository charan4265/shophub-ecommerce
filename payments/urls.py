# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<str:order_number>/',     views.payment_page,  name='payment_page'),
    path('cod/<str:order_number>/',     views.confirm_cod,   name='confirm_cod'),
    path('success/<str:order_number>/', views.payment_success, name='success'),
]