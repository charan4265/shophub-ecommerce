# accounts/views.py
# ─────────────────────────────────────────────
# Views for register, login, logout, profile
# ─────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerRegistrationForm, SellerRegistrationForm, CustomLoginForm
from .models import User


def register_buyer(request):
    """
    New buyer registration page
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = BuyerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome {user.first_name}! Your account is ready.')
        return redirect('/')

    return render(request, 'accounts/register_buyer.html', {'form': form})


def register_seller(request):
    """
    New seller registration page
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = SellerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome {user.first_name}! Please complete your store setup.')
        return redirect('sellers:setup')

    return render(request, 'accounts/register_seller.html', {'form': form})


def user_login(request):
    """
    Login page for all users
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name}!')

        # Redirect based on role
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        if user.is_seller:
            return redirect('sellers:dashboard')
        if user.is_admin_user:
            return redirect('/admin/')
        return redirect('/')

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """
    Log out and redirect to homepage
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile(request):
    """
    User profile page
    """
    return render(request, 'accounts/profile.html', {'user': request.user})