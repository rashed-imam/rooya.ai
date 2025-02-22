import { Card, CardContent, CardMedia, Typography, Button } from '@mui/material';
import { Product } from '../types/product';
import { useCart } from '../contexts/CartContext'; // Import useCart
import api from '../utils/api';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const price = typeof product.price === 'string' ? parseFloat(product.price).toFixed(2) :
                typeof product.price === 'number' ? product.price.toFixed(2) : 'N/A';
  const { updateCartCount } = useCart(); // Get updateCartCount from context

  const handleAddToCart = async (productId: number) => {
    try {
      const response = await api.post('/api/cart-items/', { product: productId, quantity: 1 });
      updateCartCount(); // Update cart count after adding item
      console.log("Item added to cart successfully", response); // Check the response
    } catch (error: any) {
      console.error("Error adding to cart:", error.response?.data || error.message); // Log detailed error
    }
  };

  return (
    <Card>
      <CardMedia
        component="img"
        height="200"
        image={`https://placehold.co/600x400?text=Product+${product.sku}`}
        alt={`Product ${product.sku}`}
      />
      <CardContent>
        <Typography gutterBottom variant="h6">
          SKU: {product.sku}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Price: ${price}
        </Typography>
        <Button variant="contained" color="primary" onClick={() => handleAddToCart(product.id)}>
          Add to Cart
        </Button>
      </CardContent>
    </Card>
  );
}