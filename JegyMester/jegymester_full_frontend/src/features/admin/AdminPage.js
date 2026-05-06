import { useQuery } from '@tanstack/react-query';
import { Alert, Stack, Typography } from '@mui/material';
import { api } from '../../api/endpoints';
import ResourceManager from './ResourceManager';

const toInt = (value) => value === '' || value === null || value === undefined ? undefined : Number(value);
const toFloat = (value) => value === '' || value === null || value === undefined ? undefined : Number(value);
const toApiDate = (value) => value ? new Date(value).toISOString() : '';

export default function AdminPage() {
  const { data: movies = [] } = useQuery({ queryKey: ['movies'], queryFn: async () => (await api.movies.list()).data });
  const { data: rooms = [] } = useQuery({ queryKey: ['rooms'], queryFn: async () => (await api.rooms.list()).data });
  const { data: screenings = [] } = useQuery({ queryKey: ['screenings'], queryFn: async () => (await api.screenings.list()).data });

  const movieOptions = movies.map((movie) => ({ value: movie.id, label: `${movie.id} - ${movie.title}` }));
  const roomOptions = rooms.map((room) => ({ value: room.id, label: `${room.id} - ${room.name}` }));
  const screeningOptions = screenings.map((screening) => ({ value: screening.id, label: `${screening.id} - film #${screening.movie_id}, terem #${screening.room_id}` }));

  return (
    <Stack spacing={3}>
      <Alert severity="info">
        Itt a backend fő funkciói kezelhetők: filmek, termek, vetítések, székek, jegyek, tranzakciók és szerepkörök.
      </Alert>
      <Typography variant="h4">Admin funkciók</Typography>

      <ResourceManager
        title="Filmek"
        queryKey="movies"
        list={api.movies.list}
        create={api.movies.create}
        update={api.movies.update}
        remove={api.movies.remove}
        fields={[
          { name: 'title', label: 'Cím', required: true },
          { name: 'description', label: 'Leírás' },
          { name: 'duration_minutes', label: 'Hossz percben', type: 'number' }
        ]}
        getCreateData={(f) => ({ ...f, duration_minutes: toInt(f.duration_minutes) })}
        getUpdateData={(f) => ({ ...f, duration_minutes: toInt(f.duration_minutes) })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'title', headerName: 'Cím', flex: 1 },
          { field: 'description', headerName: 'Leírás', flex: 1 },
          { field: 'duration_minutes', headerName: 'Perc', width: 100 }
        ]}
      />

      <ResourceManager
        title="Termek"
        queryKey="rooms"
        list={api.rooms.list}
        create={api.rooms.create}
        remove={api.rooms.remove}
        fields={[
          { name: 'name', label: 'Terem neve', required: true },
          { name: 'total_capacity', label: 'Kapacitás', type: 'number', required: true }
        ]}
        getCreateData={(f) => ({ name: f.name, total_capacity: toInt(f.total_capacity) })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'name', headerName: 'Név', flex: 1 },
          { field: 'total_capacity', headerName: 'Kapacitás', width: 130 }
        ]}
      />

      <ResourceManager
        title="Vetítések"
        queryKey="screenings"
        list={api.screenings.list}
        create={api.screenings.create}
        remove={api.screenings.remove}
        fields={[
          { name: 'movie_id', label: 'Film', required: true, options: movieOptions },
          { name: 'room_id', label: 'Terem', required: true, options: roomOptions },
          { name: 'start_time', label: 'Kezdés', type: 'datetime-local', required: true, minWidth: 220 }
        ]}
        getCreateData={(f) => ({ movie_id: toInt(f.movie_id), room_id: toInt(f.room_id), start_time: toApiDate(f.start_time) })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'movie_id', headerName: 'Film ID', width: 110 },
          { field: 'room_id', headerName: 'Terem ID', width: 110 },
          { field: 'start_time', headerName: 'Kezdés', flex: 1 }
        ]}
      />

      <ResourceManager
        title="Székek"
        queryKey="seats"
        list={api.seats.list}
        create={api.seats.create}
        remove={api.seats.remove}
        fields={[
          { name: 'room_id', label: 'Terem', required: true, options: roomOptions },
          { name: 'row_num', label: 'Sor', type: 'number', required: true },
          { name: 'seat_num', label: 'Szék', type: 'number', required: true }
        ]}
        getCreateData={(f) => ({ room_id: toInt(f.room_id), row_num: toInt(f.row_num), seat_num: toInt(f.seat_num) })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'room_id', headerName: 'Terem ID', width: 110 },
          { field: 'row_num', headerName: 'Sor', width: 90 },
          { field: 'seat_num', headerName: 'Szék', width: 90 }
        ]}
      />

      <ResourceManager
        title="Jegyek"
        queryKey="tickets"
        list={api.tickets.list}
        create={api.tickets.create}
        remove={api.tickets.remove}
        fields={[
          { name: 'transaction_id', label: 'Tranzakció ID', type: 'number', required: true },
          { name: 'screening_id', label: 'Vetítés', required: true, options: screeningOptions },
          { name: 'seat_id', label: 'Szék ID', type: 'number', required: true },
          { name: 'issued_by_id', label: 'Kiállító user ID', type: 'number' },
          { name: 'status', label: 'Státusz', defaultValue: 'valid' }
        ]}
        getCreateData={(f) => ({ transaction_id: toInt(f.transaction_id), screening_id: toInt(f.screening_id), seat_id: toInt(f.seat_id), issued_by_id: toInt(f.issued_by_id), status: f.status || 'valid' })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'transaction_id', headerName: 'Tranzakció', width: 130 },
          { field: 'screening_id', headerName: 'Vetítés', width: 110 },
          { field: 'seat_id', headerName: 'Szék', width: 90 },
          { field: 'issued_by_id', headerName: 'User', width: 100 },
          { field: 'status', headerName: 'Státusz', width: 120 }
        ]}
      />

      <ResourceManager
        title="Tranzakciók"
        queryKey="transactions"
        list={api.transactions.list}
        create={api.transactions.create}
        remove={api.transactions.remove}
        fields={[
          { name: 'user_id', label: 'User ID', type: 'number', required: true },
          { name: 'total_amount', label: 'Összeg', type: 'number', required: true },
          { name: 'payment_method', label: 'Fizetési mód', defaultValue: 'online', required: true },
          { name: 'status', label: 'Státusz', defaultValue: 'success' }
        ]}
        getCreateData={(f) => ({ user_id: toInt(f.user_id), total_amount: toFloat(f.total_amount), payment_method: f.payment_method, status: f.status || 'success' })}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'user_id', headerName: 'User', width: 100 },
          { field: 'purchase_time', headerName: 'Időpont', flex: 1 },
          { field: 'total_amount', headerName: 'Összeg', width: 120 },
          { field: 'payment_method', headerName: 'Fizetés', width: 130 },
          { field: 'status', headerName: 'Státusz', width: 120 }
        ]}
      />

      <ResourceManager
        title="Szerepkörök"
        queryKey="roles"
        list={api.roles.list}
        create={api.roles.create}
        remove={api.roles.remove}
        fields={[{ name: 'name', label: 'Szerepkör neve', required: true }]}
        columns={[
          { field: 'id', headerName: 'ID', width: 80 },
          { field: 'name', headerName: 'Név', flex: 1 }
        ]}
      />
    </Stack>
  );
}
