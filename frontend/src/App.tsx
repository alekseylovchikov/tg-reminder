import { useState } from "react";
import Modal from "react-modal";
import { useReminders } from "./hooks/useReminders";
import ReminderList from "./components/ReminderList";
import ReminderForm from "./components/ReminderForm";
import EmptyState from "./components/EmptyState";
import "./App.css";

export default function App() {
  const { data: reminders, isLoading, error } = useReminders();
  const [showForm, setShowForm] = useState(false);

  if (isLoading) {
    return <div className="loader">Загрузка…</div>;
  }

  if (error) {
    return <div className="loader">Ошибка загрузки</div>;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔔 Напоминания</h1>
      </header>

      {!reminders?.length ? (
        <EmptyState />
      ) : (
        <ReminderList reminders={reminders} />
      )}

      <button className="fab" onClick={() => setShowForm(true)} aria-label="Создать напоминание">
        +
      </button>

      <Modal
        isOpen={showForm}
        onRequestClose={() => setShowForm(false)}
        className="modal-content"
        overlayClassName="modal-overlay"
        closeTimeoutMS={200}
      >
        <ReminderForm onCreated={() => setShowForm(false)} onCancel={() => setShowForm(false)} />
      </Modal>
    </div>
  );
}
