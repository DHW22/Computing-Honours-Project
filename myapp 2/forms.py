from django import forms

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

from .models import SecondHandItem
class SecondHandItemForm(forms.ModelForm):
    class Meta:
        model = SecondHandItem
        fields = ['name', 'category', 'original_price', 'current_price', 'image', 'shipping_address']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = SecondHandItem
        fields = ['shipping_address']
