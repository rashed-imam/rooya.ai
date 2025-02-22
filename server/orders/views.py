from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Discount, OrderItem, Order, CartItem
from .serializers import ProductSerializer, DiscountSerializer, OrderItemSerializer, OrderSerializer, CartItemSerializer
from .services import OrderCalculator
from django.contrib.auth.decorators import login_required
from decimal import Decimal

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access
    filterset_fields = ['sku']
    search_fields = ['sku']
    ordering_fields = ['sku', 'price']

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    filterset_fields = ['code']
    search_fields = ['code']
    ordering_fields = ['code', 'percentage']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
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

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order_data = request.data.copy()
        order_data['user'] = request.user.id
        order_data['order_id'] = Order.objects.count() + 1
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                sku=cart_item.product.sku,
                quantity=cart_item.quantity
            )

        # Clear the cart
        cart_items.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    # Removed default permission_classes

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve', 'summary']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        # For authenticated users, filter by user
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(user=self.request.user)
        else:
            # For anonymous users, attempt to filter by session key (or other identifier)
            session_key = self.request.session.session_key
            if session_key:
                return CartItem.objects.filter(session_key=session_key)
            else:
                return CartItem.objects.none()  # Or handle the case where there's no session

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        subtotal = sum(item['total'] for item in serializer.data)
        return Response({'cart_items': serializer.data, 'subtotal': subtotal})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = request.data.get('product')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

        # For authenticated users, save with user
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user, product=product)
        else:
            # For anonymous users, save with session key (or other identifier)
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            serializer.save(session_key=session_key, product=product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cart_items = self.get_queryset()
        subtotal = sum(item.get_total() for item in cart_items)
        return Response({'subtotal': subtotal})

@api_view(['POST'])
@login_required # Ensure only logged-in users can add items
def create_cart_item(request):
    product_id = request.data.get('product')
    quantity = request.data.get('quantity')

    if not product_id or not quantity:
        return Response({'error': 'Product and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem.objects.create(user=request.user, product=product, quantity=quantity)
        return Response({'message': 'Item added to cart'}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log the error!  This is crucial.
        import logging
        logging.exception(e)
        return Response({'error': 'Failed to add item to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_coupon(request):
    coupon_code = request.data.get('code')
    try:
        discount = Discount.objects.get(code=coupon_code)
    except Discount.DoesNotExist:
        return Response({'error': 'Invalid coupon code'}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.get_total() for item in cart_items)
    discount_amount = subtotal * (discount.percentage / 100)
    discounted_total = subtotal - discount_amount

    return Response({'discounted_total': discounted_total}, status=status.HTTP_200_OK)
