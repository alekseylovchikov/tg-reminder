import "./EmptyState.css";

export default function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-icon">📝</div>
      <p className="empty-title">Нет напоминаний</p>
      <p className="empty-hint">
        Нажмите <strong>+</strong> чтобы создать первое
      </p>
    </div>
  );
}
