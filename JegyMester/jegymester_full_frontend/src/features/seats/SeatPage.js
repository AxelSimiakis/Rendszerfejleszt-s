import { useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Alert, Box, Button, Card, CardContent, Stack, Typography } from '@mui/material';
import { useSeats, useReserveSeats } from './useSeats';

export default function SeatPage() {
  const navigate = useNavigate();
  const { screeningId } = useParams();
  const { data: seats = [], isLoading, error } = useSeats(screeningId);
  const reserve = useReserveSeats();
  const [selected, setSelected] = useState([]);

  const groupedSeats = useMemo(() => seats.reduce((acc, seat) => {
    const row = seat.row_num;
    if (!acc[row]) acc[row] = [];
    acc[row].push(seat);
    acc[row].sort((a, b) => a.seat_num - b.seat_num);
    return acc;
  }, {}), [seats]);

  const toggleSeat = (seat) => {
    if (seat.reserved || reserve.isPending) return;
    setSelected((prev) => prev.includes(seat.id) ? prev.filter((id) => id !== seat.id) : [...prev, seat.id]);
  };

  const reserveSeats = () => {
    reserve.mutate({ screeningId, seats: selected }, { onSuccess: () => setSelected([]) });
  };

  if (isLoading) return <Alert severity="info">Székek betöltése...</Alert>;
  if (error) return <Alert severity="error">Nem sikerült betölteni a székeket. Ellenőrizd, hogy van-e szék a vetítés termében.</Alert>;

  return (
    <Card>
      <CardContent>
        <Stack spacing={2} alignItems="center">
          <Typography variant="h4">Helyválasztás</Typography>
          <Typography color="text.secondary">Vetítés azonosító: {screeningId}</Typography>

          <Box sx={{ width: 'min(640px, 100%)', background: '#ddd', textAlign: 'center', py: 1, borderRadius: 1 }}>
            VÁSZON
          </Box>

          <Box sx={{ textAlign: 'center' }}>
            {Object.keys(groupedSeats).sort((a, b) => Number(a) - Number(b)).map((row) => (
              <Box key={row} sx={{ whiteSpace: 'nowrap' }}>
                <Typography component="span" sx={{ display: 'inline-block', width: 32, mr: 1 }}>S{row}</Typography>
                {groupedSeats[row].map((seat) => (
                  <Button
                    type="button"
                    key={seat.id}
                    onClick={() => toggleSeat(seat)}
                    title={seat.label}
                    disabled={seat.reserved || reserve.isPending}
                    variant={selected.includes(seat.id) ? 'contained' : 'outlined'}
                    color={seat.reserved ? 'error' : selected.includes(seat.id) ? 'success' : 'primary'}
                    sx={{ minWidth: 42, width: 42, height: 42, m: 0.5, p: 0 }}
                  >
                    {seat.seat_num}
                  </Button>
                ))}
              </Box>
            ))}
          </Box>

          <Stack direction="row" spacing={2}>
            <Button variant="outlined" onClick={() => navigate('/customer')}>Vissza</Button>
            <Button variant="contained" disabled={!selected.length || reserve.isPending} onClick={reserveSeats}>
              {reserve.isPending ? 'Foglalás...' : `Foglalás (${selected.length})`}
            </Button>
          </Stack>

          {reserve.isSuccess && <Alert severity="success">Sikeres foglalás!</Alert>}
          {reserve.isError && <Alert severity="error">{reserve.error?.response?.data?.message || 'Nem sikerült a foglalás.'}</Alert>}
        </Stack>
      </CardContent>
    </Card>
  );
}
