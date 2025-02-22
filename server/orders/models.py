from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.conf import settings

class Product(models.Model):
    sku = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Product SKU: {self.sku} (${self.price})"

class Discount(models.Model):
    code = models.CharField(max_length=10, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Changed from (3,2) to (5,2)

    def get_discount_amount(self, subtotal):
        return (self.percentage* subtotal)

    def __str__(self):
        return f"{self.code} ({self.percentage}% off)"

class OrderItem(models.Model):
    sku = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)

    def get_total(self):
        """Calculate total for this item"""
        try:
            product = Product.objects.get(sku=self.sku)
            return product.price * self.quantity
        except Product.DoesNotExist:
            return Decimal('0.00')

    def __str__(self):
        return f"Order #{self.order.order_id} - SKU: {self.sku} (Qty: {self.quantity})"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    order_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.ForeignKey('Discount', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_summary(self):
        """Calculate order summary including subtotal, discount and total"""
        # Calculate subtotal from order items
        subtotal = sum(item.get_total() for item in self.items.all())
        
        # Calculate discount if applicable
        discount_amount = Decimal('0.00')
        if self.discount:
            # Convert percentage to decimal (e.g., 10% becomes 0.10)
            discount_amount = self.discount.get_discount_amount(subtotal)
        
        # Calculate final total
        total = subtotal - discount_amount
        
        return {
            'order_id': self.order_id,
            'subtotal': float(subtotal),
            'discount_amount': float(discount_amount),
            'total': float(total),
            'items_count': self.items.count(),
            'status': self.status,
            'discount_percentage': float(self.discount.percentage) if self.discount else 0.00
        }

    def __str__(self):
        discount_str = f" with {self.discount.code}" if self.discount else ""
        return f"Order #{self.order_id}{discount_str} - {self.status}"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Django session key
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.sku}"

    def get_total(self):
        return self.product.price * self.quantity
