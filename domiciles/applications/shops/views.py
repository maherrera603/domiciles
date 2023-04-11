from django.contrib.auth import authenticate
from django.contrib.auth import logout
from applications.clients.models import Client
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
#
from applications.users.mixins import ShopPermisoMixin
from applications.products.models import Product
from applications.products.models import Order
from applications.users.models import User
from applications.users.models import Role
from applications.users.forms import ChangePasswordForm
from .models import Shop
from .forms import ShopRegisterForm
from .forms import ShopUpdateForm


class Index(TemplateView):
    """ view of the home page """
    template_name = 'shops/index.html'
    context_object_name = 'shops'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        context['quantity'] = len(Shop.objects.obtain_all_shops())
        context['message'] = search
        context['shops'] = Shop.objects.obtain_all_shops_by_search(search)
        return context


class Register(FormView):
    """ Store Registration View """
    template_name = 'shops/register.html'
    form_class = ShopRegisterForm
    success_url = reverse_lazy('shop_app:register')

    def form_valid(self, form):
        rol = Role.objects.get_role(2)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.create_user(email=email, password=password, rol=rol)
        Shop.objects.create_enterprise(user, form)
        return super(Register, self).form_valid(form)


class PanelShop(ShopPermisoMixin, ListView):
    """ view of the panel of the shop """
    _shop: Shop
    _products: list[Product]
    template_name = 'shops/panel.html'
    login_url = reverse_lazy('users_app:logout')
    paginate_by = 50
    context_object_name = 'products'
    ordering = 'id'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        self._shop = Shop.objects.get_user(self.request.user)
        self._products = Product.objects.obtain_all_products_by_search(search, self._shop.id)
        return self._products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._shop
        context['quantity'] = len(self._products)
        return context


class UpdateShop(ShopPermisoMixin, UpdateView):
    """ view of update of data shop """
    template_name = 'shops/update.html'
    model = Shop
    form_class = ShopUpdateForm
    success_url = reverse_lazy('shop_app:panel_shop')
    login_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Shop.objects.get_user(self.request.user)
        return context


class ChangePassword(ShopPermisoMixin, FormView):
    login_url = reverse_lazy('users_app:logout')
    template_name = 'shops/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Shop.objects.get_user(self.request.user)
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_password = form.cleaned_data['new_password']
        user = self.request.user
        authenticated = authenticate(email=email, password=password)
        if authenticated:
            user.set_password(new_password)
            user.save()
        logout(self.request)
        return super(ChangePassword, self).form_valid(form)


class CartShop(ShopPermisoMixin, ListView):
    _user: None
    _clients: list[Client]
    login_url = reverse_lazy('users_app:logout')
    template_name = 'shops/cart_shop.html'
    context_object_name = 'clients'

    def get_queryset(self):
        self._user = Shop.objects.get_user(self.request.user)
        self._clients = Order.objects.get_clients_by_order(self._user)
        return self._clients

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._user
        context['quantity'] = len(self._clients)
        return context
