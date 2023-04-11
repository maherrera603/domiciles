from django.urls import path
#
from .views import Singing
from .views import Logout

app_name = 'users_app'

urlpatterns = [
    path('iniciar-sesion', Singing.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),]
