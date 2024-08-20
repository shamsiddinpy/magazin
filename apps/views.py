from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product
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
