import { useState, useEffect } from 'react';
import api from '../utils/api';

interface CartItem {
  id: number;
  product: number;
  quantity: number;
}

const CartPage = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [subtotal, setSubtotal] = useState(0);

  useEffect(() => {
    const fetchCartItems = async () => {
      try {
        const response = await api.get('/api/cart-items/');
        setCartItems(response.data);
      } catch (error) {
        console.error("Error fetching cart items:", error);
      }
    };

    const fetchCartSummary = async () => {
      try {
        const response = await api.get('/api/cart-items/summary/');
        setSubtotal(response.data.subtotal);
      } catch (error) {
        console.error("Error fetching cart summary:", error);
      }
    };

    fetchCartItems();
    fetchCartSummary();
  }, []);

  const handlePlaceOrder = async () => {
    try {
      await api.post('/api/orders/', {}); // You can add order details here
      // Redirect to order confirmation page or order history
    } catch (error) {
      console.error("Error placing order:", error);
    }
  };

  return (
    <div>
      <h2>Your Cart</h2>
      {cartItems.map((item) => (
        <div key={item.id}>
          Product ID: {item.product} - Quantity: {item.quantity}
        </div>
      ))}
      <div>
        Subtotal: ${subtotal}
        <button onClick={handlePlaceOrder}>Place Order</button>
      </div>
    </div>
  );
};

export default CartPage;