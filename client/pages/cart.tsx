import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  TextField,
  Button,
  Grid,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import Header from '../components/Header';
import Footer from '../components/Footer';
import api from '../utils/api'; // Your API client

interface CartItem {
  id: number;
  product: {
    id: number;
    sku: string;
    name: string;
    price: number;
  };
  quantity: number;
  total: number;
}

export default function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [couponCode, setCouponCode] = useState('');
  const [discountedTotal, setDiscountedTotal] = useState<number | null>(null);
  const [discountAmount, setDiscountAmount] = useState<number>(0);
  const [subtotal, setSubtotal] = useState<number>(0);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await api.get('/api/cart-items/');
        if (Array.isArray(response.data)) {
          setCartItems(response.data);
        } else if (response.data && Array.isArray(response.data.results)) {
          setCartItems(response.data.results);
        } else {
          setError('Unexpected cart data format');
          setCartItems([]);
        }
        setLoading(false);
      } catch (err: any) {
        setError('Failed to load cart');
        setLoading(false);
        setCartItems([]);
      }
    };

    fetchCart();
  }, []);

  const handleDeleteItem = async (itemId: number) => {
    try {
      await api.delete(`/api/cart-items/${itemId}/`);
      setCartItems(cartItems.filter((item) => item.id !== itemId)); // Optimistically update the UI
    } catch (error) {
      console.error('Error deleting item:', error);
      setError('Failed to delete item');
    }
  };

  const handleApplyCoupon = async () => {
    try {
      const response = await api.post('/api/apply-coupon/', { code: couponCode });
      setDiscountedTotal(parseFloat(response.data.discounted_total));
      setDiscountAmount(parseFloat(response.data.discount_amount));
      setSubtotal(parseFloat(response.data.subtotal));
      setError(''); // Clear any previous errors
    } catch (error: any) {
      setError(error.response?.data?.error || 'Failed to apply coupon');
      setDiscountedTotal(null); // Reset discounted total on error
      setDiscountAmount(0);
    }
  };

  const calculateSubtotal = () => {
    return cartItems.reduce((total, item) => total + item.product.price * item.quantity, 0);
  };

  const calculateTotalItems = () => {
    return cartItems.reduce((total, item) => total + item.quantity, 0);
  };

  const totalItems = calculateTotalItems();
  const total = discountedTotal !== null ? discountedTotal : subtotal;

  if (loading) {
    return <Typography>Loading cart...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  if (!Array.isArray(cartItems) || cartItems.length === 0) {
    return <Typography>Your cart is empty.</Typography>;
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Cart
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <List>
              {cartItems.map((item) => (
                <ListItem key={item.id}>
                  <ListItemText
                    primary={`${item.product.name} (${item.product.sku})`}
                    secondary={`Quantity: ${item.quantity} - $${typeof item.product.price === 'number' ? item.product.price.toFixed(2) : 'N/A'}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteItem(item.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6">Cart Summary</Typography>
            <Typography>Total Items: {totalItems}</Typography>
            <Typography>Subtotal: ${subtotal.toFixed(2)}</Typography>
            {discountAmount > 0 && (
              <Typography>Discount Amount: ${discountAmount.toFixed(2)}</Typography>
            )}
            {discountedTotal !== null && (
              <Typography>Discounted Total: ${discountedTotal.toFixed(2)}</Typography>
            )}
            <Box mt={2}>
              <TextField
                label="Coupon Code"
                variant="outlined"
                size="small"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={handleApplyCoupon} sx={{ ml: 1 }}>
                Apply
              </Button>
            </Box>
            {error && <Typography color="error">{error}</Typography>}
            <Typography variant="h6">Total: ${total.toFixed(2)}</Typography>
            <Box mt={2}>
              <Button variant="contained" color="secondary" fullWidth>
                Checkout
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Container>
      <Footer />
    </Box>
  );
}