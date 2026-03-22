# products/forms.py
# ─────────────────────────────────────────────
# Forms for adding and editing products
# ─────────────────────────────────────────────

from django import forms
from .models import Product, ProductImage, Category


class ProductForm(forms.ModelForm):
    """
    Form for sellers to add or edit a product
    """
    class Meta:
        model  = Product
        fields = (
            'name', 'category', 'description', 'condition',
            'price', 'original_price', 'stock', 'image', 'is_active'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Product name e.g. Samsung Galaxy S24'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your product in detail...',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00', 'step': '0.01'
            }),
            'original_price': forms.NumberInput(attrs={
                'placeholder': 'Original price (leave blank if no discount)',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'How many units do you have?'
            }),
        }
        labels = {
            'original_price': 'Original Price (for discount display)',
            'is_active':      'List this product publicly',
            'image':          'Main Product Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].empty_label = 'Select a category'


class ProductImageForm(forms.ModelForm):
    """
    Extra images for a product
    """
    class Meta:
        model  = ProductImage
        fields = ('image',)
        labels = {'image': 'Additional Image'}
        
from .models import Review

class ReviewForm(forms.ModelForm):
    """
    Form for buyers to leave a review
    """
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label='Your Rating'
    )

    class Meta:
        model  = Review
        fields = ('rating', 'title', 'comment')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Review title e.g. Great product!'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Share your experience with this product...',
                'rows': 4
            }),
        }
        labels = {
            'title':   'Review Title (optional)',
            'comment': 'Your Review',
        }