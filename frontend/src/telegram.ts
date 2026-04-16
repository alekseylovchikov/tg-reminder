interface TelegramWebApp {
  initData: string;
  initDataUnsafe: {
    user?: { id: number; first_name: string; last_name?: string };
  };
  ready(): void;
  expand(): void;
  close(): void;
  MainButton: {
    text: string;
    show(): void;
    hide(): void;
    onClick(cb: () => void): void;
    offClick(cb: () => void): void;
    showProgress(leaveActive?: boolean): void;
    hideProgress(): void;
  };
  themeParams: Record<string, string>;
}

declare global {
  interface Window {
    Telegram: { WebApp: TelegramWebApp };
  }
}

const tg = window.Telegram?.WebApp;

export function getTelegram(): TelegramWebApp | undefined {
  return tg;
}

export function getUserId(): number | null {
  return tg?.initDataUnsafe?.user?.id ?? null;
}

export function getInitData(): string {
  return tg?.initData ?? "";
}
