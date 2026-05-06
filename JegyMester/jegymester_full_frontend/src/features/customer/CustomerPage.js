import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Alert, Button, Card, CardActions, CardContent, Chip, Grid, Stack, Typography } from '@mui/material';
import { api } from '../../api/endpoints';

function formatDate(value) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString('hu-HU');
}

export default function CustomerPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { data: movies = [], isLoading: moviesLoading } = useQuery({ queryKey: ['movies'], queryFn: async () => (await api.movies.list()).data });
  const { data: rooms = [], isLoading: roomsLoading } = useQuery({ queryKey: ['rooms'], queryFn: async () => (await api.rooms.list()).data });
  const { data: screenings = [], isLoading: screeningsLoading, error } = useQuery({ queryKey: ['screenings'], queryFn: async () => (await api.screenings.list()).data });

  const movieMap = useMemo(() => new Map(movies.map((movie) => [movie.id, movie])), [movies]);
  const roomMap = useMemo(() => new Map(rooms.map((room) => [room.id, room])), [rooms]);

  const enriched = screenings.map((screening) => ({
    ...screening,
    movie: movieMap.get(screening.movie_id),
    room: roomMap.get(screening.room_id)
  }));

  if (error) return <Alert severity="error">Nem sikerült betölteni a vetítéseket.</Alert>;

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Vetítések</Typography>
      <Typography color="text.secondary">
        A vetítéslista bejelentkezés nélkül is megtekinthető. Jegyfoglaláshoz jelentkezz be.
      </Typography>

      {(moviesLoading || roomsLoading || screeningsLoading) && <Alert severity="info">Betöltés...</Alert>}
      {!screeningsLoading && enriched.length === 0 && <Alert severity="warning">Még nincs létrehozva vetítés. Admin oldalon adj hozzá filmet, termet, székeket és vetítést.</Alert>}

      <Grid container spacing={2}>
        {enriched.map((screening) => (
          <Grid item xs={12} md={6} lg={4} key={screening.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Stack spacing={1}>
                  <Typography variant="h5">{screening.movie?.title || `Film #${screening.movie_id}`}</Typography>
                  <Typography>{screening.movie?.description || 'Nincs leírás.'}</Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label={`${screening.movie?.duration_minutes || '-'} perc`} />
                    <Chip label={screening.room?.name || `Terem #${screening.room_id}`} />
                  </Stack>
                  <Typography variant="body2" color="text.secondary">
                    Kezdés: {formatDate(screening.start_time)}
                  </Typography>
                </Stack>
              </CardContent>
              <CardActions>
                <Button
                  variant="contained"
                  onClick={() => user ? navigate(`/screenings/${screening.id}/seats`) : navigate('/login')}
                >
                  {user ? 'Helyválasztás' : 'Bejelentkezés a foglaláshoz'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}
