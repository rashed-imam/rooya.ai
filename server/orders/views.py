from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Discount, OrderItem, Order
from .serializers import ProductSerializer, DiscountSerializer, OrderItemSerializer, OrderSerializer
from .services import OrderCalculator

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sku']
    search_fields = ['sku']
    ordering_fields = ['sku', 'price']

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['code']
    search_fields = ['code']
    ordering_fields = ['code', 'percentage']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'order_id']
    search_fields = ['order_id']
    ordering_fields = ['created_at', 'order_id']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def calculate_total(self, request, pk=None):
        order = self.get_object()
        result = OrderCalculator.calculate_order_total(order)
        return Response(result)

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        orders = Order.objects.all()
        total_sales = sum(
            float(OrderCalculator.calculate_order_total(order)['total']) 
            for order in orders
        )
        return Response({
            'total_orders': orders.count(),
            'total_sales': str(total_sales)
        })
