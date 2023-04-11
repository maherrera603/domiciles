from django import forms
from django.forms import ModelForm
#
from .models import Client


class RegisterClientForm(ModelForm):
    email = forms.CharField(
        label="Correo electronico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))

    equalPassword = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Client
        exclude = ('user', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'type_document': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_type_document(self):
        type_document = self.cleaned_data['type_document']
        if type_document == '0':
            self.add_error('type_document', 'documento no seleccionado')
        return type_document

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 12:
            self.add_error(
                'password', 'La contraseña no debe ser menor a 8 ni mayor a 12 caracteres')
        return password

    def clean_equalPassword(self):
        password = self.cleaned_data['password']
        equalPassword = self.cleaned_data['equalPassword']

        if password != equalPassword:
            self.add_error('equalPassword', 'Las contraseñas no coinciden')
        return equalPassword


class ClientForm(ModelForm):

    class Meta:
        model = Client
        exclude = ('user', 'created_at', 'updated_at')
        labels = {
            'name': 'Nombres',
            'lastname': 'Apellidos',
            'type_document': 'Tipo de documento',
            'document': 'Numero de documento',
            'phone': 'Telefono',
            'address': 'Direccion'
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control'}),

            'lastname': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control'}),

            'type_document': forms.Select(
                attrs={'class': 'form-select'}),

            'document': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control',
                       'readonly': 'readonly'}),

            'phone': forms.TextInput(
                attrs={'type': 'tel', 'class': 'form-control'}),

            'address': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control'})

        }

    def clean_address(self):
        address = self.cleaned_data['address']

        if len(address) < 5:
            self.add_error('address', 'Ingrese una direccion valida')
        return address
