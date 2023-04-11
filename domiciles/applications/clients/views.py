from django.contrib.auth import authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import UpdateView
#
from applications.users.models import Role
from applications.users.models import User
from applications.shops.models import Shop
from applications.products.models import Product
from applications.products.models import Order
from .models import Client
from .forms import RegisterClientForm
from .forms import ClientForm
from applications.users.forms import ChangePasswordForm
from applications.users.mixins import ClientPermisoMixin


# Create your views here.
class Register(FormView):
    model = Client
    form_class = RegisterClientForm
    template_name = 'clients/register.html'
    success_url = reverse_lazy('clients_app:register')

    def form_valid(self, form):
        rol = Role.objects.get_role(3)
        email = form.cleaned_data['email']
        password = form.cleaned_data['equalPassword']
        user = User.objects.create_user(email=email, password=password, rol=rol)
        Client.objects.register(form, user)
        return super().form_valid(form)


class PanelView(ClientPermisoMixin, TemplateView):
    template_name = 'clients/sistema.html'
    login_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        context['user'] = Client.objects.get_client(self.request.user)
        context['shops'] = Shop.objects.obtain_all_shops_by_search(search)
        return context


class UpdateClient(ClientPermisoMixin, UpdateView):
    login_url = reverse_lazy('users_app:logout')
    model = Client
    form_class = ClientForm
    template_name = 'clients/update.html'
    success_url = reverse_lazy('clients_app:panel-clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Client.objects.get_client(self.request.user)
        return context


class ChangePassword(ClientPermisoMixin, FormView):
    _client: Client
    login_url = reverse_lazy('users_app:logout')
    template_name = 'clients/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        self._client = Client.objects.get_client(self.request.user)
        context = super().get_context_data(**kwargs)
        context['user'] = self._client
        return context

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_password = form.cleaned_data['new_password']

        authenticated = authenticate(email=email, password=password)
        if authenticated:
            user.set_password(new_password)
            user.save()
        logout(self.request)
        return super(ChangePassword, self).form_valid(form)


class ListProducts(ClientPermisoMixin, ListView):
    _products: list[Product]
    template_name = 'clients/products.html'
    login_url = reverse_lazy('users_app:logout')
    context_object_name = 'products'

    def get_queryset(self):
        pk = self.kwargs['pk']
        search = self.request.GET.get('search', '')
        self._products = Product.objects.obtain_all_products_by_search(search, pk)
        return self._products

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['user'] = Client.objects.get_client(self.request.user)
        context['shop'] = Shop.objects.get_shop_by_id(pk)
        context['quantity'] = len(self._products)
        return context


class ListProductsByOrder(ClientPermisoMixin, ListView):
    _client: Client
    _products: list[Product]
    template_name = 'products/orders.html'
    context_object_name = 'products'

    def get_queryset(self):
        shop = self.kwargs['pk']
        self._client = Client.objects.get_client(self.request.user)
        self._products = Order.objects.get_products_of_orders(self._client, shop)
        return self._products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._client
        context['shop'] = Shop.objects.get_shop_by_id(self.kwargs['pk'])
        context['quantity'] = len(self._products)
        context['price_total'] = Order.objects.get_price_total_orders(self._client, self.kwargs['pk'])
        context['status'] = Order.objects.get_orders_by_client(self._client)
        return context
