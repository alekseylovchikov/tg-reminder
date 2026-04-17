import { Reminder } from "../types";
import { formatDate } from "../utils/formatDate";

export function ReminderCard({
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