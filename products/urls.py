# products/urls.py

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Public pages
    path('',                              views.product_list,        name='list'),
    path('<slug:slug>/',                  views.product_detail,      name='detail'),

    # Reviews
    path('<slug:slug>/review/',           views.add_review,          name='add_review'),
    path('review/delete/<int:review_id>/',views.delete_review,       name='delete_review'),

    # Seller product management
    path('manage/list/',                  views.seller_product_list, name='seller_products'),
    path('manage/add/',                   views.product_add,         name='add'),
    path('manage/edit/<slug:slug>/',      views.product_edit,        name='edit'),
    path('manage/delete/<slug:slug>/',    views.product_delete,      name='delete'),
]