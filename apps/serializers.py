from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from apps.models import Product, Cart, CartItem


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


class UserModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, required=True)
    email = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = 'username', 'email', 'password', 'confirm_password'

        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }

        }

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("Bu email alaqchon mavjud")
        if User.objects.filter(username=data['email']).exists():
            raise ValidationError("Bu email alaqchon mavjud")
        return data

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            return data
        raise ValidationError("Parol to'gir kelmaydi")


class LoginSerializer(Serializer):
    email = CharField(write_only=True, required=True)
    password = CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Email yoki parol noto'g'ri.")
            user = authenticate(username=user.username, password=password)
            if not user:
                raise ValidationError("Email yoki parol noto'g'ri.")
            data['user'] = user
        else:
            raise ValidationError("Email yoki parol noto'g'ri.")
        return data

    class Meta:
        fields = ('email', 'password')


class PasswordChangeSerializer(Serializer):
    old_password = CharField(write_only=True, required=True)  # Eski parol
    new_password = CharField(write_only=True, required=True)  # yangi parol o'zgartish

    def validate(self, data):
        """
        Eski parolni tasdiqlash va uning joriy foydalanuvchi paroliga mos kelishini tekshirisb beradi
        :param data:
        :return:
        """
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        user = self.context['request'].user

        if not user.check_password(old_password):
            raise ValidationError("Eski parol noto'g'ri.")

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise ValidationError({"new_password": e.messages})

        return data
