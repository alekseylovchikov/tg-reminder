import { useState } from "react";
import Modal from "react-modal";
import type { Reminder } from "../types";
import { useDeleteReminder } from "../hooks/useReminders";
import { ReminderCard } from "./ReminderCard";
import "./ReminderList.css";

export default function ReminderList({ reminders }: { reminders: Reminder[] }) {
  const deleteMutation = useDeleteReminder();
  const [deleteTarget, setDeleteTarget] = useState<Reminder | null>(null);

  const handleConfirmDelete = () => {
    if (!deleteTarget) return;
    deleteMutation.mutate(deleteTarget.id, {
      onSuccess: () => setDeleteTarget(null),
    });
  };

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
            onDelete={() => setDeleteTarget(r)}
          />
        ))}
      </section>
    );

  return (
    <div className="reminder-list">
      {renderSection("Предстоящие", upcoming)}
      {renderSection("Отправленные", sent)}

      <Modal
        isOpen={deleteTarget !== null}
        onRequestClose={() => setDeleteTarget(null)}
        className="modal-confirm"
        overlayClassName="modal-overlay-center"
        closeTimeoutMS={150}
      >
        <div className="confirm-title">Удалить напоминание?</div>
        <div className="confirm-text">
          «{deleteTarget?.title}» будет удалено без возможности восстановления.
        </div>
        <div className="confirm-actions">
          <button className="btn-cancel" onClick={() => setDeleteTarget(null)}>
            Отмена
          </button>
          <button
            className="btn-danger"
            onClick={handleConfirmDelete}
            disabled={deleteMutation.isPending}
          >
            {deleteMutation.isPending ? "Удаление…" : "Удалить"}
          </button>
        </div>
      </Modal>
    </div>
  );
}
