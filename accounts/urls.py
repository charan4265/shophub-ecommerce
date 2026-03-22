# accounts/urls.py
# ─────────────────────────────────────────────
# URL routes for accounts app
# ─────────────────────────────────────────────

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/buyer/',  views.register_buyer,  name='register_buyer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('login/',           views.user_login,       name='login'),
    path('logout/',          views.user_logout,      name='logout'),
    path('profile/',         views.profile,          name='profile'),
]