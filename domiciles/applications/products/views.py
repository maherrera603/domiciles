import datetime
#
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
#
from applications.shops.models import Shop
from applications.clients.models import Client
from .models import Product
from .models import Order
from .forms import ProductForm
from applications.users.mixins import ClientPermisoMixin
from applications.users.mixins import ShopPermisoMixin


# Create your views here.
class AddProduct(ShopPermisoMixin, FormView):
    _shop: Shop
    template_name = "products/product.html"
    form_class = ProductForm
    success_url = reverse_lazy('products_app:add_product')
    login_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        self._shop = Shop.objects.get_user(self.request.user)
        context = super().get_context_data(**kwargs)
        context['user'] = self._shop
        return context

    def form_valid(self, form):
        Product.objects.saveProduct(self._shop, form)
        return super(AddProduct, self).form_valid(form)


class UpdateProduct(ShopPermisoMixin, UpdateView):
    template_name = 'products/update.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shop_app:panel_shop')
    login_url = reverse_lazy('users_app:logout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Shop.objects.get_user(self.request.user)
        context['product'] = Product.objects.get_product(self.kwargs['pk'])
        return context


class DeleteProduct(ShopPermisoMixin, View):
    login_url = reverse_lazy('users_app:logout')

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        pk = self.kwargs['pk']
        product = Product.objects.get_product(pk=pk)
        delete = Product.objects.delete_product(product)
        return HttpResponseRedirect(reverse('shop_app:panel_shop')) if delete else HttpResponseRedirect(reverse('products_app:update_product', args=[pk]))


class AddCart(ClientPermisoMixin, View):
    login_url = reverse_lazy('shop_app:logout')

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        product = Product.objects.get_product(self.kwargs['product'])
        shop = Shop.objects.get_shop_by_id(self.kwargs['shop'])
        client = Client.objects.get_client_by_id(self.kwargs['client'])
        Order.objects.add_order(product=product, shop=shop, client=client)
        return HttpResponseRedirect(reverse('clients_app:list_products', args=[self.kwargs['shop']]))


class OrderList(ClientPermisoMixin, ListView):
    _client: Client
    _orders: list[Order]
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> Order:
        self._client = Client.objects.get_client(self.request.user)
        search = self.request.GET.get('search', None)
        self._orders = Order.objects.get_orders_by_client(self._client, search)
        return self._orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._client
        context['quantity'] = len(self._orders)
        return context


class UpdateOrder(ClientPermisoMixin, View):
    login_url = reverse_lazy('users_app:logout')

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        shop = self.kwargs['shop']
        pk = self.kwargs['pk']
        quantity = request.POST['quantity']
        order = Order.objects.get_order(shop, pk)
        order.quantity = quantity
        order.full_value = order.product.price * float(quantity)
        order.save()
        return HttpResponseRedirect(reverse('clients_app:products_by_order', args=[shop]))


class DeleteOrder(ClientPermisoMixin, View):
    login_url = reverse_lazy('users_app:logout')

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        shop = self.kwargs['shop']
        pk = self.kwargs['pk']
        order = Order.objects.get_order(shop, pk)
        order.delete()
        return HttpResponseRedirect(reverse('clients_app:products_by_order', args=[shop]))


class ProductsByClient(ClientPermisoMixin, ListView):
    _user: Shop
    _products: Order
    _client: Client
    template_name = 'orders/listShop.html'
    login_url = reverse_lazy('users_app:logout')
    context_object_name = 'products'

    def get_queryset(self) -> Product:
        self._client = Client.objects.get_client_by_id(self.kwargs['client'])
        self._user = Shop.objects.get_data_shops(self.request.user)
        self._products = Order.objects.get_products_of_orders(self._client, self._user)
        return self._products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._user
        context['client'] = self._client
        context['full_value'] = Order.objects.get_price_total_orders(self._client, self._user.id)
        return context


class ConfirmBuy(ClientPermisoMixin, View):
    login_url = reverse_lazy('users_app:logout')

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        orders = Order.objects.update_status_buy(self.kwargs['shop'], self.kwargs['client'])
        for order in orders:
            order.status = 2
            order.save()
        return HttpResponseRedirect(reverse('clients_app:list_orders'))


class SaveOrder(ShopPermisoMixin, View):
    login_url = reverse_lazy('users_app:logout')

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        client = self.kwargs['client']
        shop = self.kwargs['shop']
        orders = Order.objects.get_products_of_orders(client, shop)
        for order in orders:
            order.status = 3
            order.updated_at = datetime.datetime.now()
            # TODO: save data here
            order.save()
        return HttpResponseRedirect(reverse('products_app:sold_products'))


class SoldProducts(ShopPermisoMixin, ListView):
    _shop: Shop
    _products: Order
    login_url = reverse_lazy('users_app:logout')
    template_name = 'products/sold_products.html'
    context_object_name = 'products'
    paginate_by = 50
    ordering = 'id'
    model = "Order"

    def get_queryset(self) -> Order:
        self._shop = Shop.objects.get_user(self.request.user)
        dateSold = self.request.GET.get('date', None)
        self._products = Order.objects.get_orders_by_status_and_dateSold(self._shop, dateSold)
        return self._products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self._shop
        return context
