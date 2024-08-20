from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from apps.models import Product, Cart, CartItem


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        product = validated_data.get('product')
        quantity = validated_data.get('quantity', 1)
        user_cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
