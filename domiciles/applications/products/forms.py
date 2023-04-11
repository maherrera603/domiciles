from django import forms
from django.forms import ModelForm
#
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('shop', 'created_at', 'updated_at')
        labels = {
            'product': 'Producto',
            'description': 'Descripcion del producto',
            'avatar': 'Imagen del producto',
            'price': 'Precio del producto',
            'quantity': 'Cantidad del producto'
        }
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'cols': '5', 'rows': '5'}),

            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_product(self):
        product = self.cleaned_data['product']
        if len(product) < 5:
            self.add_error(
                'product', 'el nombre del producto debe ser mayor a 5 caracteres')

        return product

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 15:
            self.add_error(
                'description', 'La descripcion del producto debe ser mayor a 15 caracteres')
        return description

    def clean_price(self):
        price = int(self.cleaned_data['price'])
        if price <= 50:
            self.add_error(
                'price', 'El precio del producto debe ser mayor a $50')
        return str(price)

    def clean_quantity(self):
        quantity = int(self.cleaned_data['quantity'])
        if quantity < 1: 
            self.add_error('quantity', 'La cantidad debe ser mayor a 0')
        return str(quantity)
