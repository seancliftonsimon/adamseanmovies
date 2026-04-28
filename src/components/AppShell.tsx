import { AppAlerts } from "@/components/AppAlerts";
import { PrimaryNav } from "@/components/PrimaryNav";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <header className="app-shell__header">
        <div className="app-shell__brand">
          <p className="app-shell__eyebrow">Movie Vault</p>
          <h1 className="app-shell__title">📼 Adam &amp; Sean</h1>
        </div>
        <PrimaryNav variant="top" />
      </header>
      <main className="app-shell__content">
        <AppAlerts />
        {children}
      </main>
      <PrimaryNav variant="bottom" />
    </div>
  );
}
