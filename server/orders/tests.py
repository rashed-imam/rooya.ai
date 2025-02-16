from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Product, Discount, Order, OrderItem

class OrdersAPITest(APITestCase):
    def setUp(self):
        """Initialize test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create test products
        self.product1 = Product.objects.create(
            sku=1001,
            price=Decimal('10.00')
        )
        self.product2 = Product.objects.create(
            sku=1002,
            price=Decimal('20.00')
        )

        # Create test discount
        self.discount = Discount.objects.create(
            code='TEST10',
            percentage=Decimal('10.00')
        )

        # Get JWT token
        response = self.client.post('/auth/jwt/create/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_product_list(self):
        """Test product listing"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_discount_list(self):
        """Test discount listing"""
        response = self.client.get('/api/discounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_order(self):
        """Test order creation"""
        data = {
            'order_id': 1,
            'status': 'pending',
            'discount': self.discount.id,
            'items': [
                {
                    'sku': self.product1.sku,
                    'quantity': 2
                },
                {
                    'sku': self.product2.sku,
                    'quantity': 1
                }
            ]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify order was created
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

        # Verify order summary
        order = Order.objects.first()
        summary = order.get_summary()
        self.assertEqual(summary['subtotal'], float(Decimal('40.00')))  # (2 * 10) + (1 * 20)
        self.assertEqual(summary['discount_amount'], float(Decimal('4.00')))  # 10% of 40
        self.assertEqual(summary['total'], float(Decimal('36.00')))  # 40 - 4

    def test_unauthorized_access(self):
        """Test unauthorized access"""
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_filtering(self):
        """Test order filtering"""
        # Create test orders
        Order.objects.create(
            order_id=1,
            user=self.user,
            status='pending'
        )
        Order.objects.create(
            order_id=2,
            user=self.user,
            status='completed'
        )

        # Test status filter
        response = self.client.get('/api/orders/?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'pending')

    def test_order_search(self):
        """Test order searching"""
        Order.objects.create(
            order_id=12345,
            user=self.user,
            status='pending'
        )

        response = self.client.get('/api/orders/?search=12345')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['order_id'], 12345)