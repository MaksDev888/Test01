from django.db import models
from user.models import User

class Product(models.Model):
    """
    Create a model for products.
    """
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Create a model for carts.
    """
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    """
    Create a model for orders.
    """
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_price =  models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email
