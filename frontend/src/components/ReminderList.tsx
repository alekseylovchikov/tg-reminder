import { useState } from "react";
import type { Reminder } from "../types";
import { deleteReminder } from "../api";
import "./ReminderList.css";
import { ReminderCard } from "./ReminderCard";

interface Props {
  reminders: Reminder[];
  onDeleted: () => void;
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


