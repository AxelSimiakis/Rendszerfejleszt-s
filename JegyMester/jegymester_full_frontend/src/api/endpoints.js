import client from './client';

export const api = {
  register: (data) => client.post('/users/register', data),
  login: (data) => client.post('/users/login', data),
  me: () => client.get('/users/me'),
  movies: {
    list: () => client.get('/movies/'),
    create: (data) => client.post('/movies/', data),
    update: (id, data) => client.put(`/movies/${id}`, data),
    remove: (id) => client.delete(`/movies/${id}`)
  },
  rooms: {
    list: () => client.get('/rooms/'),
    create: (data) => client.post('/rooms/', data),
    remove: (id) => client.delete(`/rooms/${id}`)
  },
  screenings: {
    list: () => client.get('/screenings/'),
    create: (data) => client.post('/screenings/', data),
    remove: (id) => client.delete(`/screenings/${id}`)
  },
  seats: {
    list: () => client.get('/seats/'),
    byScreening: (screeningId) => client.get(`/seats/${screeningId}`),
    create: (data) => client.post('/seats/', data),
    remove: (id) => client.delete(`/seats/${id}`)
  },
  tickets: {
    list: () => client.get('/tickets/'),
    create: (data) => client.post('/tickets/', data),
    reserve: (data) => client.post('/tickets/reserve', data),
    remove: (id) => client.delete(`/tickets/${id}`)
  },
  transactions: {
    list: () => client.get('/transactions/'),
    create: (data) => client.post('/transactions/', data),
    remove: (id) => client.delete(`/transactions/${id}`)
  },
  roles: {
    list: () => client.get('/roles/'),
    create: (data) => client.post('/roles/', data),
    remove: (id) => client.delete(`/roles/${id}`)
  }
};
