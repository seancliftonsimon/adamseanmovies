"use client";

import {
  startTransition,
  useRef,
  useState,
} from "react";
import { useRouter } from "next/navigation";
import { PageIntro } from "@/components/PageIntro";
import { Poster } from "@/components/Poster";
import { useToast } from "@/components/ToastProvider";
import { LIST_TYPE_LABELS, LIST_TYPE_SHORT_LABELS } from "@/lib/constants";
import type { MovieListType, MovieRecord, MovieSearchResult } from "@/lib/types";
import { truncateText } from "@/lib/utils";

type SearchResponse = {
  results: MovieSearchResult[];
  totalResults: number;
};

const LIST_ORDER: MovieListType[] = ["adam_pick", "mutual", "sean_pick"];

export function AddMovieView() {
  const router = useRouter();
  const { pushToast } = useToast();
  const [listType, setListType] = useState<MovieListType>("adam_pick");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MovieSearchResult[]>([]);
  const [totalResults, setTotalResults] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionAddedIds, setSessionAddedIds] = useState<number[]>([]);
  const [addingTmdbId, setAddingTmdbId] = useState<number | null>(null);
  const searchTimeout = useRef<number | null>(null);
  const searchAbort = useRef<AbortController | null>(null);

  async function runSearch(searchQuery: string, signal: AbortSignal) {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `/api/tmdb/search?query=${encodeURIComponent(searchQuery.trim())}`,
        { signal },
      );
      if (!response.ok) {
        throw new Error("Search failed.");
      }

      const payload = (await response.json()) as SearchResponse;
      setResults(payload.results.slice(0, 12));
      setTotalResults(payload.totalResults);
    } catch (searchError) {
      if (signal.aborted) {
        return;
      }
      setResults([]);
      setTotalResults(0);
      setError(searchError instanceof Error ? searchError.message : "Search failed.");
    } finally {
      if (!signal.aborted) {
        setLoading(false);
      }
    }
  }

  async function handleAdd(tmdbId: number) {
    setAddingTmdbId(tmdbId);

    try {
      const response = await fetch("/api/movies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tmdbId, listType }),
      });

      const payload = (await response.json()) as
        | { movie?: MovieRecord; existing?: MovieRecord; error?: string }
        | undefined;

      if (response.status === 409 && payload?.existing) {
        pushToast({
          tone: "error",
          title: `${payload.existing.title} is already here`,
          message: `${LIST_TYPE_LABELS[payload.existing.listType]} (${payload.existing.watched ? "watched" : "unwatched"})`,
        });
        return;
      }

      if (!response.ok || !payload?.movie) {
        throw new Error(payload?.error ?? "Could not add the movie.");
      }

      setSessionAddedIds((current) => [...current, tmdbId]);
      pushToast({
        tone: "success",
        title: `Added ${payload.movie.title}`,
        message: `Saved to ${LIST_TYPE_LABELS[payload.movie.listType]}.`,
      });
      startTransition(() => {
        router.refresh();
      });
    } catch (addError) {
      pushToast({
        tone: "error",
        title: "Could not add that movie",
        message: addError instanceof Error ? addError.message : "Unknown error.",
      });
    } finally {
      setAddingTmdbId(null);
    }
  }

  return (
    <div className="stack">
      <PageIntro
        kicker="Add a Movie"
        title="Stock the Shelves"
        support="Search TMDb, preview the essentials, and drop each movie onto Adam’s shelf, Sean’s shelf, or the mutual pile."
      />

      <section className="panel stack">
        <div>
          <p className="section-label">1. Choose a shelf</p>
          <div className="pill-group">
            {LIST_ORDER.map((value) => (
              <button
                key={value}
                className="pill"
                data-active={value === listType}
                type="button"
                onClick={() => setListType(value)}
              >
                {LIST_TYPE_SHORT_LABELS[value]}
              </button>
            ))}
          </div>
        </div>

        <label className="stack">
          <span className="section-label">2. Search for a movie</span>
          <input
            className="field"
            placeholder="Eternal Sunshine, Party Girl, The Grand Budapest Hotel..."
            value={query}
            onChange={(event) => {
              const nextQuery = event.currentTarget.value;
              setQuery(nextQuery);

              if (searchTimeout.current) {
                window.clearTimeout(searchTimeout.current);
              }
              searchAbort.current?.abort();

              if (!nextQuery.trim()) {
                setResults([]);
                setTotalResults(0);
                setError(null);
                setLoading(false);
                searchAbort.current = null;
                return;
              }

              setLoading(true);
              const controller = new AbortController();
              searchAbort.current = controller;
              searchTimeout.current = window.setTimeout(() => {
                void runSearch(nextQuery, controller.signal);
              }, 250);
            }}
          />
        </label>
      </section>

      {!query.trim() ? null : (
        <section className="stack">
          {loading ? (
            <div className="status-banner">
              <p className="summary-count">Searching TMDb...</p>
              <p className="summary-copy">Pulling the first page of results.</p>
            </div>
          ) : null}

          {error ? (
            <div className="status-banner status-banner--error">
              <p className="section-title">Search failed</p>
              <p className="muted-copy">{error}</p>
            </div>
          ) : null}

          {!loading && !error && results.length > 0 ? (
            <div className="status-banner">
              <p className="summary-count">
                Showing {results.length} of {totalResults} results
              </p>
            </div>
          ) : null}

          {!loading && !error && results.length === 0 ? (
            <div className="empty-state">
              <h3 className="empty-state__title">No movies found</h3>
            </div>
          ) : null}

          <div className="movie-grid">
            {results.map((movie) => {
              const releaseYear = movie.releaseDate?.slice(0, 4) ?? "?";
              const isSessionAdded = sessionAddedIds.includes(movie.id);
              const isBusy = addingTmdbId === movie.id;

              return (
                <article key={movie.id} className="movie-card">
                  <Poster posterPath={movie.posterPath} size="w185" title={movie.title} variant="thumb" />
                  <div className="stack" style={{ gap: "0.7rem" }}>
                    <div>
                      <h3 className="movie-card__title">
                        {movie.title} ({releaseYear})
                      </h3>
                      {movie.overview ? (
                        <p className="movie-card__overview">{truncateText(movie.overview, 100)}</p>
                      ) : null}
                    </div>
                    <div className="inline-actions">
                      <button
                        className={isSessionAdded ? "button-secondary" : "button"}
                        disabled={isBusy || isSessionAdded}
                        type="button"
                        onClick={() => handleAdd(movie.id)}
                      >
                        {isSessionAdded
                          ? "Added!"
                          : isBusy
                            ? "Adding..."
                            : `Add to ${LIST_TYPE_LABELS[listType]}`}
                      </button>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}
