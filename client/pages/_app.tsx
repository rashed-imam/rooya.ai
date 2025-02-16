import type { AppProps } from 'next/app';
import { CssBaseline } from '@mui/material';
import { AuthProvider } from '../contexts/AuthContext';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../theme/index';  // Updated import path

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Component {...pageProps} />
      </ThemeProvider>
    </AuthProvider>
  );
}

export default MyApp;
