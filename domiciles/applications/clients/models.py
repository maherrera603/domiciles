from django.db import models
from django.db.models import Model
#
from applications.users.models import User
from .managers import ClientManagers


# Create your models here.
class Client(Model):

    TYPE_DOCUMENT = (
        ('0', 'Seleccione tipo de documento...'),
        ('1', 'Cedula de ciudadania'),
        ('2', 'Tarjeta de identidad')
    )

    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    type_document = models.CharField(max_length=40, choices=TYPE_DOCUMENT, default=0)
    document = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)
    user = models.ForeignKey(User, related_name='client_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ClientManagers()

    def get_full_name(self):
        return f'{self.name} {self.lastname}'

    def __str__(self):
        return f'{self.id } {self.name}'
