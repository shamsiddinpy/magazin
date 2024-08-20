from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, DestroyAPIView, get_object_or_404, GenericAPIView, \
    UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Cart, CartItem
from apps.serializers import ProductModelSerializer, CartItemCreateSerializer, LoginSerializer, PasswordChangeSerializer
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


@extend_schema(tags=['Cart'])
class CartModelViewSet(UpdateAPIView):
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
class CartUpdateAPIView(UpdateAPIView):
    serializer_class = CartItemCreateSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.save(cart_item=cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Cart'])
class CartDestroyAPIView(DestroyAPIView):

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=kwargs['pk'], cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Authentication'])
class UserRegistrationView(CreateAPIView):
    serializer_class = UserModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)


@extend_schema(tags=['Authentication'])
class UserLoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


@extend_schema(tags=['Authentication'])
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Parol muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK)
