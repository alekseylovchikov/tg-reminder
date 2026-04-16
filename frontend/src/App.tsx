import { useCallback, useEffect, useState } from "react";
import type { Reminder } from "./types";
import { fetchReminders } from "./api";
import ReminderList from "./components/ReminderList";
import ReminderForm from "./components/ReminderForm";
import EmptyState from "./components/EmptyState";
import "./App.css";

export default function App() {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const load = useCallback(async () => {
    try {
      const data = await fetchReminders();
      setReminders(data);
    } catch (e) {
      console.error("Failed to load reminders", e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleCreated = () => {
    setShowForm(false);
    load();
  };

  const handleDeleted = () => {
    load();
  };

  if (loading) {
    return <div className="loader">Загрузка…</div>;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔔 Напоминания</h1>
      </header>

      {showForm ? (
        <ReminderForm onCreated={handleCreated} onCancel={() => setShowForm(false)} />
      ) : (
        <>
          {reminders.length === 0 ? (
            <EmptyState />
          ) : (
            <ReminderList reminders={reminders} onDeleted={handleDeleted} />
          )}
          <button className="fab" onClick={() => setShowForm(true)} aria-label="Создать напоминание">
            +
          </button>
        </>
      )}
    </div>
  );
}
