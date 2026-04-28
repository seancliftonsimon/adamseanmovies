"use client";

import { Poster } from "@/components/Poster";
import type { MovieRecord } from "@/lib/types";
import { formatDate, formatRuntime } from "@/lib/utils";

type MovieDetailsDialogProps = {
  movie: MovieRecord | null;
  open: boolean;
  titlePrefix?: string;
  footer?: React.ReactNode;
  onClose: () => void;
};

export function MovieDetailsDialog({
  movie,
  open,
  titlePrefix,
  footer,
  onClose,
}: MovieDetailsDialogProps) {
  if (!open || !movie) {
    return null;
  }

  return (
    <div className="dialog-backdrop" role="presentation">
      <div className="dialog-card" role="dialog" aria-modal="true" aria-labelledby="movie-dialog-title">
        <div className="stack">
          <div className="layout-split" style={{ gridTemplateColumns: "minmax(0, 0.9fr) minmax(0, 1.25fr)" }}>
            <Poster posterPath={movie.posterPath} title={movie.title} />
            <div className="stack">
              <div>
                {titlePrefix ? <p className="panel__kicker">{titlePrefix}</p> : null}
                <h3 id="movie-dialog-title" className="movie-detail__title">
                  {movie.title} {movie.year ? `(${movie.year})` : ""}
                </h3>
              </div>
              <div className="meta-band">
                {movie.director ? <span className="meta-pill">Dir. {movie.director}</span> : null}
                {movie.runtime ? <span className="meta-pill">{formatRuntime(movie.runtime)}</span> : null}
                {movie.watchedDate ? <span className="meta-pill">{formatDate(movie.watchedDate)}</span> : null}
              </div>
              {movie.genresList.length ? (
                <div className="movie-card__meta">
                  {movie.genresList.map((genre) => (
                    <span key={genre} className="meta-pill">
                      {genre}
                    </span>
                  ))}
                </div>
              ) : null}
              {movie.overview ? <p className="movie-detail__overview">{movie.overview}</p> : null}
              {movie.notes ? <p className="muted-copy">📝 {movie.notes}</p> : null}
            </div>
          </div>
          <div className="inline-actions">
            {footer}
            <button className="button-secondary" type="button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
