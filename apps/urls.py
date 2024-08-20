from django.urls import path, include
from rest_framework import routers

from apps.views import ProductModelViewSet, UserRegistrationView, CartModelViewSet, CartDestroyAPIView, \
    UserLoginGenericAPIView, PasswordChangeView

router = routers.SimpleRouter(False)
router.register(r'products', ProductModelViewSet, basename='products')
# router.register(r'cart', CartModelView/Set, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('cart', CartModelViewSet.as_view(), name='cart'),
    path('cart/<int:pk>', CartDestroyAPIView.as_view(), name='cart_id'),
    path('sign-up', UserRegistrationView.as_view(), name='sign-up'),
    path('login', UserLoginGenericAPIView.as_view(), name='login'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),

]
