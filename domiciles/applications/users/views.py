from django.views.generic.edit import FormView
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.urls import reverse
from django.urls import reverse_lazy
#
from .forms import LoginForm


class Singing(FormView):
    _user: None
    template_name = 'users/login.html'
    form_class = LoginForm
    # success_url = reverse_lazy('shop_app:panel_shop')

    def form_valid(self, form) -> HttpResponseRedirect:
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        self._user = authenticate(email=email, password=password)
        login(self.request, self._user)
        return super(Singing, self).form_valid(form)

    def get_success_url(self):
        user_rol: bool = self._user.rol.id == 2
        panel_shop: str = 'shop_app:panel_shop'
        panel_client: str = 'clients_app:panel-clients'
        return reverse_lazy(panel_shop) if user_rol else reverse_lazy(panel_client)


class Logout(View):
    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        logout(request)
        return HttpResponseRedirect(reverse('users_app:login'))
