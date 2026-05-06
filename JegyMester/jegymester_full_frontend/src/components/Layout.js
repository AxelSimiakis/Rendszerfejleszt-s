import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const navStyle = ({ isActive }) => ({
    color: '#fff',
    textDecoration: 'none',
    fontWeight: isActive ? 700 : 400,
    marginRight: 16
  });

  const handleLogout = () => {
    logout();
    navigate('/customer', { replace: true });
  };

  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, cursor: 'pointer' }} onClick={() => navigate('/customer')}>
            JegyMester
          </Typography>

          <NavLink to="/customer" style={navStyle}>Vetítések</NavLink>
          {user && <NavLink to="/admin" style={navStyle}>Admin</NavLink>}

          {user ? (
            <>
              <Typography variant="body2" sx={{ mr: 2 }}>{user.email}</Typography>
              <Button color="inherit" onClick={handleLogout}>Kijelentkezés</Button>
            </>
          ) : (
            <Button color="inherit" onClick={() => navigate('/login')}>Bejelentkezés</Button>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
