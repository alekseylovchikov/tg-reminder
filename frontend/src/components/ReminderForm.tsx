import { useState } from "react";
import type { ReminderFormData } from "../types";
import { createReminder } from "../api";
import "./ReminderForm.css";

interface Props {
  onCreated: () => void;
  onCancel: () => void;
}

function getMinDatetime(): string {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 1);
  now.setSeconds(0, 0);
  return toLocalISO(now);
}

function toLocalISO(d: Date): string {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function ReminderForm({ onCreated, onCancel }: Props) {
  const [form, setForm] = useState<ReminderFormData>({
    title: "",
    description: "",
    remind_at: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!form.title.trim()) {
      setError("Введите название");
      return;
    }
    if (!form.remind_at) {
      setError("Выберите дату и время");
      return;
    }
    if (new Date(form.remind_at) <= new Date()) {
      setError("Нельзя выбрать прошедшее время");
      return;
    }

    setSubmitting(true);
    try {
      await createReminder(form);
      onCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка при создании");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="reminder-form" onSubmit={handleSubmit}>
      <h2>Новое напоминание</h2>

      <div className="field">
        <label htmlFor="title">Название</label>
        <input
          id="title"
          type="text"
          placeholder="О чём напомнить?"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          autoFocus
        />
      </div>

      <div className="field">
        <label htmlFor="desc">Описание</label>
        <textarea
          id="desc"
          placeholder="Подробности (необязательно)"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
      </div>

      <div className="field">
        <label htmlFor="datetime">Дата и время</label>
        <input
          id="datetime"
          type="datetime-local"
          min={getMinDatetime()}
          value={form.remind_at}
          onChange={(e) => setForm({ ...form, remind_at: e.target.value })}
        />
      </div>

      {error && <div className="form-error">{error}</div>}

      <div className="form-actions">
        <button type="button" className="btn-secondary" onClick={onCancel}>
          Отмена
        </button>
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? "Создание…" : "Создать"}
        </button>
      </div>
    </form>
  );
}
