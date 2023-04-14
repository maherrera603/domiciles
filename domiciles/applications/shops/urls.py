from django.urls import path

# views
from .views import Index
from .views import Register
from .views import PanelShop
from .views import UpdateShop
from .views import CartShop
from .views import ChangePassword

app_name = 'shop_app'

urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('registrar-empresa', Register.as_view(), name='register'),

    path('sistema/', PanelShop.as_view(), name='panel_shop'),

    path('actualizar-datos/<int:pk>', UpdateShop.as_view(), name='update_shop'),

    path('pedidos/', CartShop.as_view(), name='cart_shop'),

    path('actualizar-contraseña', ChangePassword.as_view(), name='change_password'),
]
