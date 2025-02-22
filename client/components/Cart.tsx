import { useState, useEffect } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  Button,
  Typography,
  Box,
  CircularProgress
} from '@mui/material';
import api from '../utils/api';

interface CartItem {
  id: number;
  product: number;
  quantity: number;
}

export default function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCartItems = async () => {
      try {
        const response = await api.get('/api/cart-items/');
        setCartItems(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load cart items');
        setLoading(false);
      }
    };

    fetchCartItems();
  }, []);

  const handleRemoveFromCart = async (itemId: number) => {
    try {
      await api.delete(`/api/cart-items/${itemId}/`);
      setCartItems(cartItems.filter((item) => item.id !== itemId));
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" m={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box m={4}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <List>
      {cartItems.map((item) => (
        <ListItem key={item.id}>
          <ListItemText primary={`Product ID: ${item.product}`} secondary={`Quantity: ${item.quantity}`} />
          <Button variant="outlined" color="secondary" onClick={() => handleRemoveFromCart(item.id)}>
            Remove
          </Button>
        </ListItem>
      ))}
    </List>
  );
}