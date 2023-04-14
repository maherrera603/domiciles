from django.contrib.auth import authenticate
from django import forms
from django.forms import Form


class LoginForm(Form):
    email = forms.CharField(
        label='Correo electronico',
        widget=forms.TextInput({'class': 'form-control', 'type': 'email'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.TextInput({'class': 'form-control', 'type': 'password'})
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 12:
            self.add_error('password', 'La contraseña no debe ser menor a 8 ni mayor a 12 caracteres')
        return password

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos son incorrectos')
        return cleaned_data


class ChangePasswordForm(Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control',
                   'required': 'required'}))

    password = forms.CharField(
            label='Contraseña Actual',
            widget=forms.TextInput(
                attrs={'type': 'password', 'class': 'form-control',
                       'required': 'required'}))

    new_password = forms.CharField(
            label='Nueva contraseña',
            widget=forms.TextInput(
                attrs={'type': 'password', 'class': 'form-control',
                       'required': 'required'}))

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8 or len(password) > 12:
            self.add_error('password', 'La contraseña debe contener de 8 a 12 caracteres')
        return password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        if len(new_password) < 8 or len(new_password) > 12:
            self.add_error('new_password', 'La nueva contraseña debe contener de 8 a 12 caracteres')
        return new_password

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = self.cleaned_data['password']
        new_password = self.cleaned_data['new_password']

        if password == new_password:
            self.add_error('new_password', 'La contraseña ya se uso anteriormente, intentelo de nuevo')
        return cleaned_data
