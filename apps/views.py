from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Cart, CartItem
from apps.serializers import ProductModelSerializer, CartItemCreateSerializer
from apps.serializers import UserModelSerializer


# Create your views here.

@extend_schema(tags=['Products'])
class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        return Product.objects.all()


@extend_schema(tags=['Register'])
class UserRegistrationView(CreateAPIView):
    serializer_class = UserModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            headers = self.get_success_headers(serializer.data)
            return Response({
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Cart'])
class CartModelViewSet(ListCreateAPIView):
    serializer_class = CartItemCreateSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Cart'])
class CartDestroyAPIView(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=kwargs['pk'], cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
