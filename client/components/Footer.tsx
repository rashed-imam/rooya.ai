import { Box, Container, Typography, Link } from '@mui/material';

export default function Footer() {
  return (
    <Box component="footer" sx={{ bgcolor: 'background.paper', py: 6, mt: 'auto' }}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {'© '}
          <Link color="inherit" href="/">
            E-Shop
          </Link>{' '}
          {new Date().getFullYear()}
        </Typography>
      </Container>
    </Box>
  );
}