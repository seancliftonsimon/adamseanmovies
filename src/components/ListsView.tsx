"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MovieDetailsDialog } from "@/components/MovieDetailsDialog";
import { PageIntro } from "@/components/PageIntro";
import { Poster } from "@/components/Poster";
import { WatchDialog } from "@/components/WatchDialog";
import { useToast } from "@/components/ToastProvider";
import {
  LIST_TYPE_LABELS,
  SHELF_SORT_OPTIONS,
} from "@/lib/constants";
import { sortShelfMovies, type ShelfSortOption } from "@/lib/movie-filters";
import type { MovieListType, MovieRecord, WatchPayload } from "@/lib/types";

const SHELVES: MovieListType[] = ["adam_pick", "sean_pick", "mutual"];

export function ListsView({ initialMovies }: { initialMovies: MovieRecord[] }) {
  const router = useRouter();
  const { pushToast } = useToast();
  const [movies, setMovies] = useState(initialMovies);
  const [activeShelf, setActiveShelf] = useState<MovieListType>("adam_pick");
  const [sorts, setSorts] = useState<Record<MovieListType, ShelfSortOption>>({
    adam_pick: "Recently Added",
    sean_pick: "Recently Added",
    mutual: "Recently Added",
  });
  const [detailMovie, setDetailMovie] = useState<MovieRecord | null>(null);
  const [watchMovie, setWatchMovie] = useState<MovieRecord | null>(null);
  const [removePending, setRemovePending] = useState(false);
  const [watchBusy, setWatchBusy] = useState(false);
  const [confirmingRemove, setConfirmingRemove] = useState(false);

  const shelfMovies = sortShelfMovies(
    movies.filter((movie) => movie.listType === activeShelf),
    sorts[activeShelf],
  );

  async function handleRemove() {
    if (!detailMovie) {
      return;
    }

    setRemovePending(true);

    try {
      const response = await fetch(`/api/movies/${detailMovie.id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const body = (await response.json()) as { error?: string };
        throw new Error(body.error ?? "Could not remove the movie.");
      }

      setMovies((current) => current.filter((movie) => movie.id !== detailMovie.id));
      pushToast({
        tone: "success",
        title: `${detailMovie.title} removed`,
      });
      setDetailMovie(null);
      setConfirmingRemove(false);
      router.refresh();
    } catch (error) {
      pushToast({
        tone: "error",
        title: "Could not remove that movie",
        message: error instanceof Error ? error.message : "Unknown error.",
      });
    } finally {
      setRemovePending(false);
    }
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
        throw new Error(body.error ?? "Could not mark the movie watched.");
      }

      setMovies((current) => current.filter((movie) => movie.id !== watchMovie.id));
      setWatchMovie(null);
      setDetailMovie(null);
      pushToast({
        tone: "success",
        title: `${watchMovie.title} moved to the Watch Log`,
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

  return (
    <div className="stack">
      <PageIntro
        kicker="Our Lists"
        title="Browse the Shelves"
        support="Flip between Adam’s picks, Sean’s picks, and the shared stack, then sort each shelf your own way."
      />

      <section className="panel stack">
        <div>
          <p className="section-label">Choose a shelf</p>
          <div className="tab-row">
            {SHELVES.map((shelf) => (
              <button
                key={shelf}
                className="pill"
                data-active={shelf === activeShelf}
                type="button"
                onClick={() => setActiveShelf(shelf)}
              >
                {shelf === "mutual" ? "Mutual" : LIST_TYPE_LABELS[shelf]}
              </button>
            ))}
          </div>
        </div>

        <label className="stack">
          <span className="field-label">Sort shelf</span>
          <select
            className="select"
            value={sorts[activeShelf]}
            onChange={(event) =>
              setSorts((current) => ({
                ...current,
                [activeShelf]: event.currentTarget.value as ShelfSortOption,
              }))
            }
          >
            {SHELF_SORT_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </section>

      <section className="stack">
        <div className="status-banner">
          <p className="summary-count">{shelfMovies.length} movie(s)</p>
        </div>

        {!shelfMovies.length ? (
          <div className="empty-state">
            <h3 className="empty-state__title">This shelf is empty</h3>
          </div>
        ) : (
          <div className="shelf-grid">
            {shelfMovies.map((movie) => (
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
          </div>
        )}
      </section>

      <MovieDetailsDialog
        footer={
          detailMovie ? (
            <>
              <button className="button" type="button" onClick={() => setWatchMovie(detailMovie)}>
                We watched this!
              </button>
              {confirmingRemove ? (
                <button className="button-danger" disabled={removePending} type="button" onClick={handleRemove}>
                  {removePending ? "Removing..." : "Yes, remove"}
                </button>
              ) : (
                <button className="button-danger" type="button" onClick={() => setConfirmingRemove(true)}>
                  Remove
                </button>
              )}
              {confirmingRemove ? (
                <button
                  className="button-secondary"
                  disabled={removePending}
                  type="button"
                  onClick={() => setConfirmingRemove(false)}
                >
                  Cancel remove
                </button>
              ) : null}
            </>
          ) : null
        }
        movie={detailMovie}
        open={Boolean(detailMovie)}
        titlePrefix="Shelf Details"
        onClose={() => {
          setDetailMovie(null);
          setConfirmingRemove(false);
        }}
      />

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
