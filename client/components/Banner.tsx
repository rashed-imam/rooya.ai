import { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';
import api from '../utils/api';

interface Discount {
  id: number;
  code: string;
  percentage: number;
}

export default function Banner() {
  const [currentDiscount, setCurrentDiscount] = useState<Discount | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDiscount = async () => {
      try {
        const response = await api.get('/api/discounts/');
        if (response.data.results && response.data.results.length > 0) {
          const randomIndex = Math.floor(Math.random() * response.data.results.length);
          setCurrentDiscount(response.data.results[randomIndex]);
          setLoading(false);
        } else {
          setError('No discounts available');
          setLoading(false);
        }
      } catch (err) {
        setError('Failed to load discount');
        setLoading(false);
      }
    };

    fetchDiscount();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 1,
          textAlign: 'center',
        }}
      >
        Loading discount...
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        sx={{
          bgcolor: 'error.main',
          color: 'white',
          py: 1,
          textAlign: 'center',
        }}
      >
        {error}
      </Box>
    );
  }

  return (
    <Box
      sx={{
        bgcolor: 'primary.main',
        color: 'white',
        py: 1,
        textAlign: 'center',
      }}
    >
      {currentDiscount && (
        <Typography variant="body2">
          Use code <strong>{currentDiscount.code}</strong> for{' '}
          {currentDiscount.percentage}% off!
        </Typography>
      )}
    </Box>
  );
}