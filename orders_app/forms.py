from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, product=None, **kwargs):
        self.product = product
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if self.product and qty > self.product.stock:
            raise forms.ValidationError(
                f"Only {self.product.stock} item(s) available in stock."
            )
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return qty


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
