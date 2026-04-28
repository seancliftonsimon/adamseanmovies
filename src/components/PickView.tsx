"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
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
import { getPosterUrl } from "@/lib/posters";
import type { MovieRecord, WatchPayload } from "@/lib/types";
import { formatRuntime, formatRuntimeCompact } from "@/lib/utils";

const REVEAL_DURATION_MS = 9200;
const REVEAL_POSTER_LIMIT = 18;

function pickRandom<T>(items: T[]) {
  return items[Math.floor(Math.random() * items.length)];
}

function shuffled<T>(items: T[]) {
  return [...items].sort(() => Math.random() - 0.5);
}

function buildRevealContenders(movies: MovieRecord[], winner: MovieRecord) {
  const contenders = shuffled(movies).slice(0, REVEAL_POSTER_LIMIT);

  if (!contenders.some((movie) => movie.id === winner.id)) {
    contenders[contenders.length ? contenders.length - 1 : 0] = winner;
  }

  return shuffled(contenders);
}

function posterSource(movie: MovieRecord, size = "w342") {
  return getPosterUrl(movie.posterPath, size) ?? "/poster-placeholder.svg";
}

type RevealRun = {
  winner: MovieRecord;
  contenders: MovieRecord[];
};

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
  const [revealRun, setRevealRun] = useState<RevealRun | null>(null);
  const [spotlightIndex, setSpotlightIndex] = useState(0);
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

  useEffect(() => {
    if (!revealRun) {
      return;
    }

    const posterTimer = window.setInterval(() => {
      setSpotlightIndex((current) => current + 1);
    }, 135);

    const timer = window.setTimeout(() => {
      setPickedMovie(revealRun.winner);
      setRevealRun(null);
      setIsRevealing(false);
      window.requestAnimationFrame(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }, REVEAL_DURATION_MS);

    return () => {
      window.clearInterval(posterTimer);
      window.clearTimeout(timer);
    };
  }, [revealRun]);

  function runReveal() {
    if (!filteredMovies.length || isRevealing) {
      return;
    }

    const winner = pickRandom(filteredMovies);
    setPickedMovie(null);
    setSpotlightIndex(0);
    setRevealRun({
      winner,
      contenders: buildRevealContenders(filteredMovies, winner),
    });
    setIsRevealing(true);
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
      {revealRun ? (() => {
        const activeSpotlightIndex = spotlightIndex % revealRun.contenders.length;

        return (
        <div className="pick-reveal-modal" role="dialog" aria-modal="true" aria-label="Choosing tonight's movie">
          <div className="pick-reveal-modal__card">
            <div className="pick-reveal-modal__lights" aria-hidden="true" />

            <div className="pick-reveal-filmstrips" aria-hidden="true">
              {[0, 1, 2].map((row) => (
                <div className="pick-reveal-filmstrip" data-direction={row === 1 ? "reverse" : "forward"} key={row}>
                  {[...revealRun.contenders, ...revealRun.contenders].map((movie, index) => (
                    <div className="pick-reveal-filmstrip__poster" key={`${row}-${movie.id}-${index}`}>
                      <Image alt="" height={278} src={posterSource(movie, "w185")} width={185} />
                    </div>
                  ))}
                </div>
              ))}
            </div>

            <div className="pick-reveal-spotlight" aria-hidden="true">
              {revealRun.contenders.map((movie, index) => (
                <div
                  className="pick-reveal-spotlight__card"
                  data-active={index === activeSpotlightIndex}
                  key={movie.id}
                >
                  <Image alt="" height={513} priority={index === 0} src={posterSource(movie)} width={342} />
                </div>
              ))}
            </div>

            <div className="pick-reveal-winner">
              <Image alt="" height={750} priority src={posterSource(revealRun.winner, "w500")} width={500} />
            </div>
          </div>
        </div>
        );
      })() : null}

      <PageIntro
        kicker={null}
        title="Pick For Us"
        support="Filter by shelf, genre, or runtime, then let the tape machine decide tonight’s movie."
      />

      {pickedMovie ? (
        <section className="panel detail-sheet">
          <div>
            <p className="page-intro__kicker" style={{ marginBottom: "0.85rem" }}>
              Tonight&apos;s Movie
            </p>
            <div className="detail-sheet__grid">
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
