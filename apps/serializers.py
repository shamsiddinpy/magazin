from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from apps.models import Product, Cart, CartItem


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'password'

        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("Bu email alaqchon mavjud")
        return data


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartModelSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(ModelSerializer):
    cart = CartModelSerializer(many=False)
    product = ProductModelSerializer(read_only=True, many=False)

    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemCreateSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart = self.context['cart']
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
