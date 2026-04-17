import type { Reminder } from "../types";
import { useDeleteReminder } from "../hooks/useReminders";
import "./ReminderList.css";
import { ReminderCard } from "./ReminderCard";

interface Props {
  reminders: Reminder[];
}

export default function ReminderList({ reminders }: Props) {
  const deleteMutation = useDeleteReminder();

  const upcoming = reminders.filter((r) => !r.is_sent);
  const sent = reminders.filter((r) => r.is_sent);

  const renderSection = (title: string, items: Reminder[]) =>
    items.length > 0 && (
      <section>
        <h2 className="section-title">{title}</h2>
        {items.map((r) => (
          <ReminderCard
            key={r.id}
            reminder={r}
            deleting={deleteMutation.isPending && deleteMutation.variables === r.id}
            onDelete={() => deleteMutation.mutate(r.id)}
          />
        ))}
      </section>
    );

  return (
    <div className="reminder-list">
      {renderSection("Предстоящие", upcoming)}
      {renderSection("Отправленные", sent)}
    </div>
  );
}
