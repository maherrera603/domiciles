from django.urls import path
#
from .views import AddProduct
from .views import UpdateProduct
from .views import DeleteProduct
from .views import AddCart
from .views import UpdateOrder
from .views import DeleteOrder
from .views import ProductsByClient
from .views import ConfirmBuy
from .views import SaveOrder
from .views import SoldProducts

app_name = 'products_app'

urlpatterns = [
    path(
        'agregar-producto',
        AddProduct.as_view(),
        name='add_product'),

    path(
        'actualizar-producto/<int:pk>/',
        UpdateProduct.as_view(),
        name='update_product'),

    path(
        'eliminar-producto/<int:pk>/',
        DeleteProduct.as_view(),
        name='delete_product'),

    path(
        'agregar-orden/<int:product>/<int:shop>/<int:client>',
        AddCart.as_view(),
        name='add_cart'),

    path(
        'update_order/<int:shop>/<int:pk>',
        UpdateOrder.as_view(),
        name="update_order"),

    path(
        'delete_order/<int:shop>/<int:pk>',
        DeleteOrder.as_view(),
        name="delete_order"),

    path(
        'pedidos/<int:shop>/<int:client>',
        ProductsByClient.as_view(),
        name="order_client"),

    path(
        'compra/<int:shop>/<int:client>',
        ConfirmBuy.as_view(),
        name='confirm_buy'),

    path(
        'saveBuy/<int:shop>/<int:client>',
        SaveOrder.as_view(),
        name='save_order'),

    path(
        'ventas/',
        SoldProducts.as_view(),
        name='sold_products'),]
