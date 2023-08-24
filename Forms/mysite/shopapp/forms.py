from django import forms
from django.contrib.auth.models import User
from django.core import validators

from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = 'name', 'price', 'description', 'discount'
        # Product.description = forms.CharField(
        #     widget=forms.Textarea(attrs={'rows': 5, 'cols': 10})
        # )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        # fields = 'delivery_address', 'promocode', 'products'
        # Order.user = forms.ModelChoiceField(
        #     queryset=User.objects.all(),
        # )