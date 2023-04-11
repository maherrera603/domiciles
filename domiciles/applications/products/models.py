from django.db import models
#
from applications.shops.models import Shop
from applications.clients.models import Client
from .managers import ProductManager
from .managers import OrderManager


# Create your models here.
class Product(models.Model):
    product = models.CharField(max_length=50)
    description = models.TextField()
    avatar = models.ImageField(upload_to='products')
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, related_name='product_shop', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ProductManager()

    def __str__(self):
        return f'{self.id} {self.product}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('1', 'Pendiente'),
        ('2', 'Confirmada'),
        ('3', 'Vendido')
    )
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='order_shop', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='order_client', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    full_value = models.FloatField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = OrderManager()

    def __str__(self):
        return f'{self.id}'
