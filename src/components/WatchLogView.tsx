"use client";

import { useState } from "react";
import { MovieDetailsDialog } from "@/components/MovieDetailsDialog";
import { PageIntro } from "@/components/PageIntro";
import { Poster } from "@/components/Poster";
import { WATCH_LOG_VIEWS } from "@/lib/constants";
import type { MovieRecord, WatchStats } from "@/lib/types";
import { ratingToStars } from "@/lib/utils";

type LogView = (typeof WATCH_LOG_VIEWS)[number];

function StatCard({
  label,
  value,
  accent = false,
}: {
  label: string;
  value: string | number;
  accent?: boolean;
}) {
  return (
    <article className={`stat-card${accent ? " stat-card--accent" : ""}`}>
      <p className="stat-card__label">{label}</p>
      <h3 className="stat-card__value">{value}</h3>
    </article>
  );
}

export function WatchLogView({
  watched,
  stats,
}: {
  watched: MovieRecord[];
  stats: WatchStats;
}) {
  const [view, setView] = useState<LogView>("Overview");
  const [detailMovie, setDetailMovie] = useState<MovieRecord | null>(null);

  if (!watched.length) {
    return (
      <div className="stack">
        <PageIntro
          kicker="Watch Log"
          title="Watched Together"
          support="As soon as you log a movie from Pick or Lists, it lands here with your ratings and notes."
        />
        <div className="empty-state">
          <h3 className="empty-state__title">No watched movies yet</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="stack">
      <PageIntro
        kicker="Watch Log"
        title="Watched Together"
        support="Look back at everything you’ve seen together, plus the stats that make the whole habit feel real."
      />

      <section className="panel panel--tight">
        <p className="section-label">Choose a view</p>
        <div className="segmented">
          {WATCH_LOG_VIEWS.map((option) => (
            <button
              key={option}
              className="pill"
              data-active={option === view}
              type="button"
              onClick={() => setView(option)}
            >
              {option}
            </button>
          ))}
        </div>
      </section>

      {view === "Overview" ? (
        <section className="stats-grid">
          <StatCard accent label="Movies Watched" value={stats.total} />
          <StatCard label="Total Hours" value={`${stats.totalHours}h`} />
          <StatCard label="Adam's Avg" value={stats.avgAdam ? `${stats.avgAdam}/10` : "—"} />
          <StatCard label="Sean's Avg" value={stats.avgSean ? `${stats.avgSean}/10` : "—"} />
          <StatCard label="Top Genre" value={stats.topGenre || "—"} />
          <StatCard label="Adam's Picks Done" value={stats.adamSuggestedWatched} />
          <StatCard label="Sean's Picks Done" value={stats.seanSuggestedWatched} />
        </section>
      ) : (
        <section className="shelf-grid">
          {watched.map((movie) => (
            <article key={movie.id} className="vhs-card">
              <Poster posterPath={movie.posterPath} size="w185" title={movie.title} />
              <div className="vhs-card__label">
                <h3 className="vhs-card__title">{movie.title}</h3>
                <p className="vhs-card__meta">{movie.year ?? "?"}</p>
              </div>
              <button className="button-secondary" type="button" onClick={() => setDetailMovie(movie)}>
                Details
              </button>
            </article>
          ))}
        </section>
      )}

      <MovieDetailsDialog
        footer={
          detailMovie ? (
            <div className="stack" style={{ gap: "0.45rem" }}>
              <span className="meta-pill">Adam: {ratingToStars(detailMovie.adamRating)}</span>
              <span className="meta-pill">Sean: {ratingToStars(detailMovie.seanRating)}</span>
            </div>
          ) : null
        }
        movie={detailMovie}
        open={Boolean(detailMovie)}
        titlePrefix="Watched"
        onClose={() => setDetailMovie(null)}
      />
    </div>
  );
}
