import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../../api/endpoints';

export const useSeats = (screeningId) =>
  useQuery({
    queryKey: ['seats', screeningId],
    enabled: Boolean(screeningId),
    queryFn: async () => (await api.seats.byScreening(screeningId)).data
  });

export const useReserveSeats = () => {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: ({ screeningId, seats }) =>
      api.tickets.reserve({
        screening_id: Number(screeningId),
        seat_ids: seats.map(Number)
      }),
    onSuccess: (_, vars) => {
      qc.invalidateQueries({ queryKey: ['seats', vars.screeningId] });
      qc.invalidateQueries({ queryKey: ['tickets'] });
      qc.invalidateQueries({ queryKey: ['transactions'] });
    }
  });
};
