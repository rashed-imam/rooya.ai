import { AppBar, Toolbar, Typography, Button, Badge } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';
import { useCart } from '../contexts/CartContext';

export default function Header() {
  const { isAuthenticated, logout } = useAuth();
  const { cartCount } = useCart();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link href="/" passHref>
            <span style={{ color: 'white', textDecoration: 'none' }}>
              E-Shop
            </span>
          </Link>
        </Typography>
        <Button color="inherit" component="a" href="/products">
          Products
        </Button>
        {isAuthenticated ? (
          <>
            <Button color="inherit" component="a" href="/dashboard">
              Dashboard
            </Button>
            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          </>
        ) : (
          <Button color="inherit" component="a" href="/login">
            Login
          </Button>
        )}
        <Link href="/cart" passHref>
          <Button color="inherit">
            <Badge badgeContent={cartCount} color="error">
              <ShoppingCartIcon />
            </Badge>
          </Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
}