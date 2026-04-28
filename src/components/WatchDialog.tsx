"use client";

import { useState } from "react";
import type { WatchPayload } from "@/lib/types";

type WatchDialogProps = {
  movieTitle: string;
  open: boolean;
  busy?: boolean;
  onClose: () => void;
  onSubmit: (payload: WatchPayload) => Promise<void> | void;
};

function todayIsoDate() {
  return new Date().toISOString().slice(0, 10);
}

export function WatchDialog({
  movieTitle,
  open,
  busy = false,
  onClose,
  onSubmit,
}: WatchDialogProps) {
  const [adamRating, setAdamRating] = useState(7);
  const [seanRating, setSeanRating] = useState(7);
  const [notes, setNotes] = useState("");
  const [watchedDate, setWatchedDate] = useState(todayIsoDate());

  if (!open) {
    return null;
  }

  return (
    <div className="dialog-backdrop" role="presentation">
      <div className="dialog-card" role="dialog" aria-modal="true" aria-labelledby="watch-dialog-title">
        <div className="stack">
          <div>
            <p className="panel__kicker">Watch Log</p>
            <h3 id="watch-dialog-title" className="movie-detail__title">
              Rate {movieTitle}
            </h3>
          </div>

          <label className="stack">
            <span className="field-label">Adam&apos;s rating: {adamRating}/10</span>
            <input
              max={10}
              min={1}
              type="range"
              value={adamRating}
              onChange={(event) => setAdamRating(Number(event.currentTarget.value))}
            />
          </label>

          <label className="stack">
            <span className="field-label">Sean&apos;s rating: {seanRating}/10</span>
            <input
              max={10}
              min={1}
              type="range"
              value={seanRating}
              onChange={(event) => setSeanRating(Number(event.currentTarget.value))}
            />
          </label>

          <label className="stack">
            <span className="field-label">Notes</span>
            <textarea
              className="textarea"
              placeholder="Great pick, wild ending, perfect Friday movie..."
              value={notes}
              onChange={(event) => setNotes(event.currentTarget.value)}
            />
          </label>

          <label className="stack">
            <span className="field-label">Date watched</span>
            <input
              className="field"
              type="date"
              value={watchedDate}
              onChange={(event) => setWatchedDate(event.currentTarget.value)}
            />
          </label>

          <div className="inline-actions">
            <button
              className="button"
              disabled={busy}
              type="button"
              onClick={() => onSubmit({ adamRating, seanRating, notes, watchedDate })}
            >
              {busy ? "Saving..." : "Save to Watch Log"}
            </button>
            <button className="button-secondary" disabled={busy} type="button" onClick={onClose}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
