import { useState } from "react";
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

      {showForm ? (
        <ReminderForm onCreated={() => setShowForm(false)} onCancel={() => setShowForm(false)} />
      ) : (
        <>
          {!reminders?.length ? (
            <EmptyState />
          ) : (
            <ReminderList reminders={reminders} />
          )}
          <button className="fab" onClick={() => setShowForm(true)} aria-label="Создать напоминание">
            +
          </button>
        </>
      )}
    </div>
  );
}
