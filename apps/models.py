from django.contrib.auth.models import User

# Create your models here.

from django.db.models import Model, CharField, DecimalField, IntegerField, OneToOneField, CASCADE, DateTimeField, \
    ForeignKey, PositiveIntegerField
from django_ckeditor_5.fields import CKEditor5Field


class Product(Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = CKEditor5Field(blank=True, null=True)
    stock = IntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(Model):
    user = OneToOneField(User, CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(Model):
    cart = ForeignKey('apps.Cart', related_name='items', on_delete=CASCADE)
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
