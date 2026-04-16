import type { Reminder, ReminderFormData } from "./types";
import { getInitData, getUserId } from "./telegram";

const BASE = "/api";

function headers(): HeadersInit {
  return {
    "Content-Type": "application/json",
    Authorization: getInitData(),
  };
}

export async function fetchReminders(): Promise<Reminder[]> {
  const res = await fetch(`${BASE}/reminders`, { headers: headers() });
  if (!res.ok) throw new Error(`Failed to fetch: ${res.status}`);
  return res.json();
}

export async function createReminder(data: ReminderFormData): Promise<Reminder> {
  const userId = getUserId();
  if (userId === null) throw new Error("No user id");

  const res = await fetch(`${BASE}/reminders`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      user_id: userId,
      title: data.title,
      description: data.description,
      remind_at: new Date(data.remind_at).toISOString(),
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Failed to create: ${res.status}`);
  }
  return res.json();
}

export async function deleteReminder(id: number): Promise<void> {
  const res = await fetch(`${BASE}/reminders/${id}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) throw new Error(`Failed to delete: ${res.status}`);
}
