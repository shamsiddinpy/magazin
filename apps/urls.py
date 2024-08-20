from django.urls import path, include
from rest_framework import routers

from apps.views import ProductModelViewSet, UserRegistrationView, CartModelViewSet

router = routers.SimpleRouter(False)
router.register(r'products', ProductModelViewSet, basename='products')
# router.register(r'cart', CartModelView/Set, basename='cart')
urlpatterns = [
    path('', include(router.urls)),
    path('sign-up', UserRegistrationView.as_view(), name='sign-up'),
    path('cart', CartModelViewSet.as_view(), name='cart'),
    # path('cart/<int:id>', CartItemCreateSerializer.as_view(), name='cart_id'),
]
