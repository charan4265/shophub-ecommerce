# sellers/forms.py
# ─────────────────────────────────────────────
# Forms for store setup and editing
# ─────────────────────────────────────────────

from django import forms
from .models import Store


class StoreSetupForm(forms.ModelForm):
    """
    Form shown to seller right after registration
    to set up their store for the first time
    """
    class Meta:
        model  = Store
        fields = (
            'name', 'description', 'logo',
            'email', 'phone', 'address', 'city', 'state'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your store name e.g. Chara Electronics'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Tell buyers what your store sells...',
                'rows': 4
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Store contact email'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Store phone number'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Store address',
                'rows': 2
            }),
            'city':  forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
        }
        labels = {
            'name': 'Store Name',
            'logo': 'Store Logo (optional)',
        }


class StoreEditForm(forms.ModelForm):
    """
    Form for seller to edit their store details later
    """
    class Meta:
        model  = Store
        fields = (
            'name', 'description', 'logo', 'banner',
            'email', 'phone', 'address', 'city', 'state'
        )
        widgets = {
            'name':        forms.TextInput(attrs={'placeholder': 'Store name'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'email':       forms.EmailInput(),
            'phone':       forms.TextInput(),
            'address':     forms.Textarea(attrs={'rows': 2}),
            'city':        forms.TextInput(),
            'state':       forms.TextInput(),
        }