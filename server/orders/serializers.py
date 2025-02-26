from rest_framework import serializers
from .models import Product, Discount, Order, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'price']  # Include other product details

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'percentage']

class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_total')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'sku', 'quantity', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    summary = serializers.DictField(read_only=True, source='get_summary')
    
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'user', 'status', 'discount', 'items', 'summary', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested serializer for product details
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']

    def get_total(self, obj):
        return obj.product.price * obj.quantity