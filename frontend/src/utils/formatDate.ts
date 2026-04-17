import dayjs from "dayjs";
import isToday from "dayjs/plugin/isToday";
import isTomorrow from "dayjs/plugin/isTomorrow";

dayjs.extend(isToday);
dayjs.extend(isTomorrow);

export function formatDate(iso: string): string {
  const d = dayjs(iso);
  const time = d.format("HH:mm");

  if (d.isToday()) return `сегодня ${time}`;
  if (d.isTomorrow()) return `завтра ${time}`;
  return d.format("DD/MM/YYYY HH:mm");
}
