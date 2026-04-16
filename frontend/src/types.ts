export interface Reminder {
  id: number;
  user_id: number;
  title: string;
  description: string;
  remind_at: string;
  created_at: string;
  is_sent: boolean;
}

export interface ReminderFormData {
  title: string;
  description: string;
  remind_at: string;
}
