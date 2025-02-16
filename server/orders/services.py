from decimal import Decimal
from .models import Product, Order

class OrderCalculator:
    @staticmethod
    def calculate_order_total(order: Order) -> dict:
        total = Decimal('0.00')
        items_summary = []
        
        for item in order.items.all():
            product = Product.objects.get(sku=item.sku)
            item_total = product.price * item.quantity
            total += item_total
            items_summary.append({
                'sku': item.sku,
                'quantity': item.quantity,
                'unit_price': str(product.price),
                'total': str(item_total)
            })
        
        if order.discount:
            discount_amount = total * order.discount.percentage
            total -= discount_amount
            
        return {
            'order_id': order.order_id,
            'items': items_summary,
            'discount_code': order.discount.code if order.discount else None,
            'subtotal': str(total + (discount_amount if order.discount else Decimal('0.00'))),
            'discount_amount': str(discount_amount) if order.discount else '0.00',
            'total': str(total)
        }
