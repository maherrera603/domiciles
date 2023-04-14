from django.urls import path
#
from .views import Register
from .views import PanelView
from .views import UpdateClient
from .views import ChangePassword
from .views import ListProducts
from .views import ListProductsByOrder

from applications.products.views import OrderList

app_name = 'clients_app'

urlpatterns = [
    path('registrarse/', Register.as_view(), name='register'),

    path('', PanelView.as_view(), name='panel-clients'),

    path('actualizar-datos/<int:pk>', UpdateClient.as_view(), name='update_client'),

    path('tienda/<int:pk>/', ListProducts.as_view(), name='list_products'),

    path('carrito-cliente/', OrderList.as_view(), name='list_orders'),

    path('carrito-cliente/tienda/<int:pk>/', ListProductsByOrder.as_view(), name='products_by_order'),

    path('actualizar-contraseña/', ChangePassword.as_view(), name='change_password')
]
