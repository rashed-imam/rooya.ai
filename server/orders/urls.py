from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet, OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]