"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { PageIntro } from "@/components/PageIntro";
import { Poster } from "@/components/Poster";
import { WatchDialog } from "@/components/WatchDialog";
import { useToast } from "@/components/ToastProvider";
import {
  LIST_TYPE_LABELS,
  PICK_LIST_FILTERS,
  RUNTIME_PRESETS,
} from "@/lib/constants";
import { buildActivePickFilters, filterPickMovies, type PickListFilterValue } from "@/lib/movie-filters";
import type { MovieRecord, WatchPayload } from "@/lib/types";
import { formatRuntime, formatRuntimeCompact } from "@/lib/utils";

function delay(ms: number) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function pickRandom<T>(items: T[]) {
  return items[Math.floor(Math.random() * items.length)];
}

export function PickView({
  initialMovies,
  availableGenres,
}: {
  initialMovies: MovieRecord[];
  availableGenres: string[];
}) {
  const router = useRouter();
  const { pushToast } = useToast();
  const [movies, setMovies] = useState(initialMovies);
  const [listFilter, setListFilter] = useState<PickListFilterValue>("all");
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [runtimeFilter, setRuntimeFilter] = useState<(typeof RUNTIME_PRESETS)[number]["value"]>("any");
  const [customRuntime, setCustomRuntime] = useState(150);
  const [pickedMovie, setPickedMovie] = useState<MovieRecord | null>(null);
  const [revealingMovie, setRevealingMovie] = useState<MovieRecord | null>(null);
  const [isRevealing, setIsRevealing] = useState(false);
  const [watchMovie, setWatchMovie] = useState<MovieRecord | null>(null);
  const [watchBusy, setWatchBusy] = useState(false);

  const filteredMovies = filterPickMovies(movies, {
    listFilter,
    selectedGenres,
    runtimeFilter,
    customRuntime,
  });

  const hasOptionalFilters =
    listFilter !== "all" || selectedGenres.length > 0 || runtimeFilter !== "any";

  const activeFilters = buildActivePickFilters({
    listFilter,
    selectedGenres,
    runtimeFilter,
    customRuntime,
  });

  async function runReveal() {
    if (!filteredMovies.length || isRevealing) {
      return;
    }

    setPickedMovie(null);
    setIsRevealing(true);

    for (let index = 0; index < 12; index += 1) {
      setRevealingMovie(pickRandom(filteredMovies));
      await delay(80 + index * 30);
    }

    setRevealingMovie(null);
    setPickedMovie(pickRandom(filteredMovies));
    setIsRevealing(false);
  }

  async function handleWatchSubmit(payload: WatchPayload) {
    if (!watchMovie) {
      return;
    }

    setWatchBusy(true);

    try {
      const response = await fetch(`/api/movies/${watchMovie.id}/watch`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const body = (await response.json()) as { error?: string };
        throw new Error(body.error ?? "Could not save the watch log.");
      }

      setMovies((current) => current.filter((movie) => movie.id !== watchMovie.id));
      setWatchMovie(null);
      setPickedMovie(null);
      pushToast({
        tone: "success",
        title: `${watchMovie.title} saved to the Watch Log`,
      });
      router.refresh();
    } catch (error) {
      pushToast({
        tone: "error",
        title: "Could not save the watch log",
        message: error instanceof Error ? error.message : "Unknown error.",
      });
    } finally {
      setWatchBusy(false);
    }
  }

  function toggleGenre(genre: string) {
    setSelectedGenres((current) =>
      current.includes(genre) ? current.filter((item) => item !== genre) : [...current, genre],
    );
  }

  if (!movies.length) {
    return (
      <div className="stack">
        <PageIntro kicker={null} title="Pick For Us" support="The randomizer wakes up once you have something unwatched on the shelves." />
        <div className="empty-state">
          <h3 className="empty-state__title">No unwatched movies yet</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="stack">
      <PageIntro
        kicker={null}
        title="Pick For Us"
        support="Filter by shelf, genre, or runtime, then let the tape machine decide tonight’s movie."
      />

      <div className="layout-split">
        <section className="panel stack">
          <div>
            <p className="section-label">1. Whose picks?</p>
            <div className="pill-group">
              {PICK_LIST_FILTERS.map((filter) => (
                <button
                  key={filter.value}
                  className="pill"
                  data-active={filter.value === listFilter}
                  type="button"
                  onClick={() => setListFilter(filter.value)}
                >
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="section-label">2. Genres</p>
            <div className="pill-group">
              {availableGenres.map((genre) => (
                <button
                  key={genre}
                  className="pill"
                  data-active={selectedGenres.includes(genre)}
                  type="button"
                  onClick={() => toggleGenre(genre)}
                >
                  {genre}
                </button>
              ))}
            </div>
          </div>

          <div className="stack">
            <div>
              <p className="section-label">3. Runtime</p>
              <div className="pill-group">
                {RUNTIME_PRESETS.map((preset) => (
                  <button
                    key={preset.value}
                    className="pill"
                    data-active={runtimeFilter === preset.value}
                    type="button"
                    onClick={() => setRuntimeFilter(preset.value)}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {runtimeFilter === "custom" ? (
              <label className="stack">
                <span className="field-label">Custom max runtime: {formatRuntimeCompact(customRuntime)}</span>
                <input
                  max={300}
                  min={60}
                  step={5}
                  type="range"
                  value={customRuntime}
                  onChange={(event) => setCustomRuntime(Number(event.currentTarget.value))}
                />
              </label>
            ) : null}

            {activeFilters.length ? (
              <div className="movie-card__meta">
                {activeFilters.map((filter) => (
                  <span key={filter} className="meta-pill">
                    {filter}
                  </span>
                ))}
              </div>
            ) : null}
          </div>
        </section>

        <section className="panel stack">
          {filteredMovies.length ? (
            <div>
              <p className="summary-count">{filteredMovies.length} tapes ready</p>
              <p className="summary-copy">Filtered down from your current unwatched stack.</p>
            </div>
          ) : (
            <div className="empty-state">
              <h3 className="empty-state__title">No tapes match these filters</h3>
            </div>
          )}

          {filteredMovies.length ? (
            <div className="sample-strip">
              {filteredMovies.slice(0, 3).map((movie) => (
                <Poster
                  key={movie.id}
                  posterPath={movie.posterPath}
                  size="w154"
                  title={movie.title}
                  variant="thumb"
                />
              ))}
            </div>
          ) : null}

          <button className="button" disabled={!filteredMovies.length || isRevealing} type="button" onClick={runReveal}>
            {isRevealing ? "Picking..." : "Pick for Us"}
          </button>

          {!filteredMovies.length && hasOptionalFilters ? (
            <button
              className="button-secondary"
              type="button"
              onClick={() => {
                setListFilter("all");
                setSelectedGenres([]);
                setRuntimeFilter("any");
                setCustomRuntime(150);
              }}
            >
              Clear All
            </button>
          ) : null}
        </section>
      </div>

      {isRevealing && revealingMovie ? (
        <section className="panel reveal-stage">
          <p className="reveal-stage__copy">Finding your perfect tape...</p>
          <Poster posterPath={revealingMovie.posterPath} title={revealingMovie.title} />
          <h3 className="movie-detail__title">{revealingMovie.title}</h3>
        </section>
      ) : null}

      {pickedMovie ? (
        <section className="panel detail-sheet">
          <div>
            <p className="page-intro__kicker" style={{ marginBottom: "0.85rem" }}>
              Tonight&apos;s Movie
            </p>
            <div className="layout-split" style={{ gridTemplateColumns: "minmax(0, 0.95fr) minmax(0, 1.25fr)" }}>
              <Poster posterPath={pickedMovie.posterPath} title={pickedMovie.title} priority />
              <div className="stack">
                <h3 className="movie-detail__title">{pickedMovie.title}</h3>
                <div className="meta-band">
                  {pickedMovie.year ? <span className="meta-pill">{pickedMovie.year}</span> : null}
                  {pickedMovie.director ? <span className="meta-pill">Dir. {pickedMovie.director}</span> : null}
                  {pickedMovie.runtime ? (
                    <span className="meta-pill">{formatRuntime(pickedMovie.runtime)}</span>
                  ) : null}
                  <span className="meta-pill">{LIST_TYPE_LABELS[pickedMovie.listType]}</span>
                </div>
                {pickedMovie.genresList.length ? (
                  <div className="movie-card__meta">
                    {pickedMovie.genresList.map((genre) => (
                      <span key={genre} className="meta-pill">
                        {genre}
                      </span>
                    ))}
                  </div>
                ) : null}
                {pickedMovie.overview ? (
                  <p className="movie-detail__overview">{pickedMovie.overview}</p>
                ) : null}
                <div className="inline-actions">
                  <button className="button-secondary" type="button" onClick={() => setPickedMovie(null)}>
                    Spin Again
                  </button>
                  <button className="button" type="button" onClick={() => setWatchMovie(pickedMovie)}>
                    Let&apos;s Watch This!
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      ) : null}

      <WatchDialog
        busy={watchBusy}
        key={watchMovie?.id ?? "watch-dialog"}
        movieTitle={watchMovie?.title ?? ""}
        open={Boolean(watchMovie)}
        onClose={() => setWatchMovie(null)}
        onSubmit={handleWatchSubmit}
      />
    </div>
  );
}
