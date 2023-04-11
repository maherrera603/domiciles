from django import forms
from django.forms import ModelForm
#
from .models import Shop


class ShopRegisterForm(ModelForm):
    email = forms.CharField(
        label="Correo electronico", widget=forms.EmailInput())

    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput())

    equalPassword = forms.CharField(
        label="Confirmar Contraseña", widget=forms.PasswordInput())

    class Meta:
        model = Shop
        fields = ('shop', 'nit', 'phone')

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 12:
            self.add_error('password', 'La contraseña debe ser mayor a 8 y menor a 12 caracteres')
        return password

    def clean_equalPassword(self):
        password = self.cleaned_data['password']
        equalPassword = self.cleaned_data['equalPassword']
        if equalPassword != password:
            self.add_error('equalPassword', 'Las contraseñas no coinciden')
        return equalPassword


class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ('user', 'created_at', 'updated_at')
        labels = {
            'shop': 'Nombre de la tienda',
            'avatar': 'Imagen del tienda',
            'description': 'Descripcion de la tienda',
            'phone': 'Numero de telefono',
            'address': 'Direccion de la tienda'
        }
        widgets = {
            'shop': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text'}),

            'nit': forms.TextInput(
                attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'description': forms.Textarea(
                attrs={'class': 'form-control', 'cols': '5', 'rows': '5'}),

            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'tel'}),

            'address': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text'})
        }

    def clean_shop(self):
        shop = self.cleaned_data['shop']
        if len(shop) < 5:
            self.add_error(
                'shop', 'El nombre de la tienda debe ser mayor a 5 caracteres')
        return shop

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 15:
            self.add_error('description', 'La description de la tienda debe ser mayor a 15 caracteres')
        return description

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) < 10 or len(phone) > 10:
            self.add_error('phone', 'El telefono debe tener 10 caracteres')
        return phone

    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 15:
            self.add_error(
                'address', 'La direccion de la tienda debe tener 15 caracteres o mas')
        return address

