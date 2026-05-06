import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Alert, Box, Button, Card, CardContent, Container, Stack, Tab, Tabs, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function LoginPage() {
  const { login, register: registerUser } = useAuth();
  const navigate = useNavigate();
  const loginForm = useForm();
  const registerForm = useForm();
  const [tab, setTab] = useState(0);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async (fn) => {
    setError(null);
    setLoading(true);
    try {
      await fn();
      navigate('/customer');
    } catch (err) {
      const message = err?.response?.data?.message || err?.message || 'Sikertelen művelet.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const onLogin = (data) => run(() => login(data.email, data.password));
  const onRegister = (data) => run(() => registerUser(data));

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>JegyMester</Typography>
          <Tabs value={tab} onChange={(_, value) => { setTab(value); setError(null); }} sx={{ mb: 2 }}>
            <Tab label="Belépés" />
            <Tab label="Regisztráció" />
          </Tabs>

          {tab === 0 && (
            <Box component="form" onSubmit={loginForm.handleSubmit(onLogin)}>
              <Stack spacing={2}>
                <TextField label="Email" type="email" fullWidth {...loginForm.register('email', { required: true })} />
                <TextField label="Jelszó" type="password" fullWidth {...loginForm.register('password', { required: true })} />
                <Button type="submit" variant="contained" disabled={loading}>Belépés</Button>
              </Stack>
            </Box>
          )}

          {tab === 1 && (
            <Box component="form" onSubmit={registerForm.handleSubmit(onRegister)}>
              <Stack spacing={2}>
                <TextField label="Név" fullWidth {...registerForm.register('name')} />
                <TextField label="Email" type="email" fullWidth {...registerForm.register('email', { required: true })} />
                <TextField label="Telefonszám" fullWidth {...registerForm.register('phone_number', { required: true })} />
                <TextField label="Jelszó" type="password" fullWidth {...registerForm.register('password', { required: true })} />
                <Button type="submit" variant="contained" disabled={loading}>Regisztráció és belépés</Button>
              </Stack>
            </Box>
          )}

          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
        </CardContent>
      </Card>
    </Container>
  );
}
