# orders/forms.py
# ─────────────────────────────────────────────
# Checkout address form
# ─────────────────────────────────────────────

from django import forms


class CheckoutForm(forms.Form):
    """
    Delivery address form shown at checkout
    """
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'House no, Street, Area',
            'rows': 3
        })
    )
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'State'})
    )
    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'PIN code'})
    )