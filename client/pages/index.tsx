import { useState, useEffect } from 'react';
import { Container, Grid, Typography, Box, CircularProgress } from '@mui/material';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ProductCard from '../components/ProductCard';
import api from '../utils/api';
import { Product } from '../types/product';

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await api.get('/api/products/');
        setProducts(response.data.results);
        setLoading(false);
      } catch (err) {
        setError('Failed to load products');
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Featured Products
        </Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" m={4}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : (
          <Grid container spacing={4}>
            {products.map((product) => (
              <Grid item key={product.id} xs={12} sm={6} md={4}>
                <ProductCard product={product} />
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
      <Footer />
    </Box>
  );
}
