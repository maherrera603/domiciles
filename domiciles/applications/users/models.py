from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# manager the user
from .managers import UserManager
from .managers import RoleManager


# Create your models here.
class Role(models.Model):
    rol = models.CharField(max_length=20)
    objects = RoleManager()

    def __str__(self):
        return f'{self.rol}'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, related_name='rol_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    # field required for valiation the user
    USERNAME_FIELD = 'email'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
