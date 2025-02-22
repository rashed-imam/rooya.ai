from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet, OrderItemViewSet, OrderViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]