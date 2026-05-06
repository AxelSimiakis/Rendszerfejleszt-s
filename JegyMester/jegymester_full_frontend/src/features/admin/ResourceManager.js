import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, Button, Card, CardContent, CircularProgress, Divider, MenuItem, Stack, TextField, Typography } from '@mui/material';

const fieldType = (field) => field.type || 'text';

function formatValue(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

export default function ResourceManager({ title, queryKey, list, create, update, remove, fields, columns, getCreateData, getUpdateData }) {
  const qc = useQueryClient();
  const [form, setForm] = useState(() => Object.fromEntries(fields.map((field) => [field.name, field.defaultValue ?? ''])));
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState(null);

  const { data = [], isLoading, error } = useQuery({
    queryKey: [queryKey],
    queryFn: async () => (await list()).data
  });

  const reset = () => {
    setForm(Object.fromEntries(fields.map((field) => [field.name, field.defaultValue ?? ''])));
    setEditingId(null);
  };

  const mutationOptions = {
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: [queryKey] });
      setMessage('Sikeres mentés.');
      reset();
    },
    onError: (err) => setMessage(err?.response?.data?.message || 'Hiba történt.')
  };

  const createMutation = useMutation({ mutationFn: (payload) => create(payload), ...mutationOptions });
  const updateMutation = useMutation({ mutationFn: ({ id, payload }) => update(id, payload), ...mutationOptions });
  const deleteMutation = useMutation({
    mutationFn: (id) => remove(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [queryKey] }),
    onError: (err) => setMessage(err?.response?.data?.message || 'Nem sikerült a törlés.')
  });

  const rows = useMemo(() => Array.isArray(data) ? data : [], [data]);

  const gridColumns = [
    ...columns,
    {
      field: 'actions',
      headerName: 'Műveletek',
      width: update ? 210 : 130,
      sortable: false,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          {update && (
            <Button size="small" onClick={() => {
              setEditingId(params.row.id);
              setForm(Object.fromEntries(fields.map((field) => [field.name, params.row[field.name] ?? field.defaultValue ?? ''])));
            }}>
              Szerkeszt
            </Button>
          )}
          <Button color="error" size="small" onClick={() => deleteMutation.mutate(params.row.id)}>
            Törlés
          </Button>
        </Stack>
      )
    }
  ];

  const submit = (event) => {
    event.preventDefault();
    setMessage(null);
    const dataToSend = editingId && getUpdateData ? getUpdateData(form) : getCreateData ? getCreateData(form) : form;
    if (editingId && update) updateMutation.mutate({ id: editingId, payload: dataToSend });
    else createMutation.mutate(dataToSend);
  };

  const busy = createMutation.isPending || updateMutation.isPending || deleteMutation.isPending;

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>{title}</Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>Nem sikerült betölteni.</Alert>}
        {message && <Alert severity={message.includes('Sikeres') ? 'success' : 'error'} sx={{ mb: 2 }}>{message}</Alert>}

        <Box component="form" onSubmit={submit} sx={{ mb: 2 }}>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems="stretch">
            {fields.map((field) => (
              <TextField
                key={field.name}
                label={field.label}
                type={fieldType(field)}
                select={Boolean(field.options)}
                value={form[field.name] ?? ''}
                onChange={(event) => setForm((prev) => ({ ...prev, [field.name]: event.target.value }))}
                required={field.required}
                sx={{ minWidth: field.minWidth || 180 }}
                InputLabelProps={field.type === 'datetime-local' ? { shrink: true } : undefined}
              >
                {(field.options || []).map((option) => (
                  <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                ))}
              </TextField>
            ))}
            <Button type="submit" variant="contained" disabled={busy} sx={{ minWidth: 140 }}>
              {busy ? <CircularProgress size={22} /> : editingId ? 'Mentés' : 'Hozzáadás'}
            </Button>
            {editingId && <Button onClick={reset}>Mégse</Button>}
          </Stack>
        </Box>

        <Divider sx={{ mb: 2 }} />
        <div style={{ height: 420, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={gridColumns.map((col) => ({ ...col, valueFormatter: col.valueFormatter || ((value) => formatValue(value)) }))}
            loading={isLoading}
            disableRowSelectionOnClick
            pageSizeOptions={[5, 10, 25]}
            initialState={{ pagination: { paginationModel: { pageSize: 5 } } }}
          />
        </div>
      </CardContent>
    </Card>
  );
}
