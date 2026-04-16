import { useState } from "react";
import type { Reminder } from "../types";
import { deleteReminder } from "../api";
import "./ReminderList.css";

interface Props {
  reminders: Reminder[];
  onDeleted: () => void;
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function ReminderList({ reminders, onDeleted }: Props) {
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const handleDelete = async (id: number) => {
    setDeletingId(id);
    try {
      await deleteReminder(id);
      onDeleted();
    } catch (e) {
      console.error("Delete failed", e);
    } finally {
      setDeletingId(null);
    }
  };

  const upcoming = reminders.filter((r) => !r.is_sent);
  const sent = reminders.filter((r) => r.is_sent);

  return (
    <div className="reminder-list">
      {upcoming.length > 0 && (
        <section>
          <h2 className="section-title">Предстоящие</h2>
          {upcoming.map((r) => (
            <ReminderCard
              key={r.id}
              reminder={r}
              deleting={deletingId === r.id}
              onDelete={() => handleDelete(r.id)}
            />
          ))}
        </section>
      )}
      {sent.length > 0 && (
        <section>
          <h2 className="section-title">Отправленные</h2>
          {sent.map((r) => (
            <ReminderCard
              key={r.id}
              reminder={r}
              deleting={deletingId === r.id}
              onDelete={() => handleDelete(r.id)}
            />
          ))}
        </section>
      )}
    </div>
  );
}

function ReminderCard({
  reminder,
  deleting,
  onDelete,
}: {
  reminder: Reminder;
  deleting: boolean;
  onDelete: () => void;
}) {
  return (
    <div className={`reminder-card ${reminder.is_sent ? "sent" : ""}`}>
      <div className="reminder-content">
        <div className="reminder-title">{reminder.title}</div>
        {reminder.description && (
          <div className="reminder-desc">{reminder.description}</div>
        )}
        <div className="reminder-time">⏰ {formatDate(reminder.remind_at)}</div>
      </div>
      <button
        className="delete-btn"
        onClick={onDelete}
        disabled={deleting}
        aria-label="Удалить"
      >
        {deleting ? "…" : "✕"}
      </button>
    </div>
  );
}
