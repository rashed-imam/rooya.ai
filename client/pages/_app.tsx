import type { AppProps } from 'next/app';
import { CssBaseline } from '@mui/material';
import { AuthProvider } from '../contexts/AuthContext';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../theme/index';
import { CartProvider } from '@/contexts/CartContext';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <CartProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Component {...pageProps} />
        </ThemeProvider>
      </CartProvider>
    </AuthProvider>
  );
}

export default MyApp;
