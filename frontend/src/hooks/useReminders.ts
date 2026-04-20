import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchReminders, createReminder, deleteReminder } from "../api";
import type { ReminderFormData } from "../types";

const REMINDERS_KEY = ["reminders"] as const;

export function useReminders() {
  return useQuery({
    queryKey: REMINDERS_KEY,
    queryFn: fetchReminders,
  });
}

export function useCreateReminder() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ReminderFormData) => createReminder(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: REMINDERS_KEY }),
  });
}

export function useDeleteReminder() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteReminder(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: REMINDERS_KEY }),
  });
}
