from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


def check_ocupation_user(rol, rol_user) -> bool:
    print(f'desde los mixins {rol} {rol_user} {type(rol)} {rol == rol_user}')
    return rol.rol == rol_user


class ClientPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:logout')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        rol_user = 'Cliente'
        if not check_ocupation_user(request.user.rol, rol_user):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:logout'
                )
            )

        return super().dispatch(request, *args, **kwargs)


class ShopPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:logout')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        rol_user = 'Empresa'
        if not check_ocupation_user(request.user.rol, rol_user):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:logout'
                )
            )
        return super().dispatch(request, *args, **kwargs)
