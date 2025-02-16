import { Card, CardContent, CardMedia, Typography, Button, Box } from '@mui/material';
import { Product } from '../types/product';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <Card>
      <CardMedia
        component="img"
        height="200"
        image={`https://source.unsplash.com/random?product=${product.sku}`}
        alt={`Product ${product.sku}`}
      />
      <CardContent>
        <Typography gutterBottom variant="h6">
          SKU: {product.sku}
        </Typography>
        <Typography variant="h5" color="primary">
          ${product.price.toFixed(2)}
        </Typography>
        <Box mt={2}>
          <Button variant="contained" color="primary" fullWidth>
            Add to Cart
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}