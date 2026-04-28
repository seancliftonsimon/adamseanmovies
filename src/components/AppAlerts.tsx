import { getStorageGuardrailStatus } from "@/lib/movies";

export async function AppAlerts() {
  let warning:
    | {
        count: number;
        maxMovies: number;
      }
    | null = null;
  let errorDetail: string | null = null;

  try {
    const storage = await getStorageGuardrailStatus();
    if (storage.percentUsed >= 90) {
      warning = {
        count: storage.count,
        maxMovies: storage.maxMovies,
      };
    }
  } catch (error) {
    errorDetail = error instanceof Error ? error.message : "Unknown database error";
  }

  if (warning) {
    return (
      <section className="status-banner status-banner--warning" style={{ marginBottom: "1rem" }}>
        <p className="section-title" style={{ marginBottom: "0.35rem" }}>
          Storage guardrail is nearly full
        </p>
        <p className="muted-copy" style={{ marginTop: 0 }}>
          {warning.count} of {warning.maxMovies} movies are already stored. Consider clearing older
          entries before adding more.
        </p>
      </section>
    );
  }

  if (!errorDetail) {
    return null;
  }

  return (
    <section className="status-banner status-banner--error" style={{ marginBottom: "1rem" }}>
      <p className="section-title" style={{ marginBottom: "0.35rem" }}>
        Database setup is incomplete
      </p>
      <p className="muted-copy" style={{ marginTop: 0 }}>
        The app could not reach Postgres. Check `DATABASE_URL` and confirm the Neon connection is
        available.
      </p>
      <p className="muted-copy" style={{ marginTop: "0.5rem" }}>
        Detail: {errorDetail}
      </p>
    </section>
  );
}
