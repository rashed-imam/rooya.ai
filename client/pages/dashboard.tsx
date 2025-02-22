import DashboardLayout from '../components/DashboardLayout';
import { Typography, Container } from '@mui/material';

export default function Dashboard() {
  return (
    <DashboardLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography>Welcome to your dashboard!</Typography>
      </Container>
    </DashboardLayout>
  );
}