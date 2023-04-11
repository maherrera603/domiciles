from django.db import models
from django.db.models import Model
#
from applications.users.models import User
from .managers import ShopsManager


# Create your models here.
class Shop(Model):
    shop = models.CharField(max_length=50)
    nit = models.IntegerField(unique=True)
    avatar = models.ImageField(upload_to='shops', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)
    user = models.ForeignKey(User, related_name='shop_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ShopsManager()

    def __str__(self):
        return f'{self.id} {self.shop}'
