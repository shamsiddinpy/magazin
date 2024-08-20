from django.contrib import admin

from apps.models import Product, Cart, CartItem


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class ProductAdmin(admin.ModelAdmin):
    pass
