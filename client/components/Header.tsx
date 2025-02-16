import { AppBar, Toolbar, Typography, Button, Badge } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

export default function Header() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link href="/" style={{ color: 'white', textDecoration: 'none' }}>
            E-Shop
          </Link>
        </Typography>
        <Button color="inherit" component={Link} href="/products">
          Products
        </Button>
        {isAuthenticated ? (
          <>
            <Button color="inherit" component={Link} href="/dashboard">
              Dashboard
            </Button>
            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          </>
        ) : (
          <Button color="inherit" component={Link} href="/login">
            Login
          </Button>
        )}
        <Button color="inherit">
          <Badge badgeContent={0} color="error">
            <ShoppingCartIcon />
          </Badge>
        </Button>
      </Toolbar>
    </AppBar>
  );
}