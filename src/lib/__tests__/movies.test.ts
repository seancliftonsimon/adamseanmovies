import { describe, expect, it } from "vitest";
import { computeWatchStatsFromMovies } from "@/lib/watch-stats";
import type { MovieRecord } from "@/lib/types";

const WATCHED_MOVIES: MovieRecord[] = [
  {
    id: 1,
    tmdbId: 11,
    title: "Movie One",
    year: 2000,
    posterPath: null,
    director: null,
    genres: '["Drama","Romance"]',
    genresList: ["Drama", "Romance"],
    runtime: 120,
    overview: null,
    listType: "adam_pick",
    addedBy: "Adam",
    addedDate: "2025-01-01T00:00:00Z",
    watched: true,
    watchedDate: "2025-02-01",
    adamRating: 8,
    seanRating: 7,
    notes: null,
  },
  {
    id: 2,
    tmdbId: 12,
    title: "Movie Two",
    year: 2001,
    posterPath: null,
    director: null,
    genres: '["Drama"]',
    genresList: ["Drama"],
    runtime: 90,
    overview: null,
    listType: "sean_pick",
    addedBy: "Sean",
    addedDate: "2025-01-02T00:00:00Z",
    watched: true,
    watchedDate: "2025-02-02",
    adamRating: 6,
    seanRating: 9,
    notes: null,
  },
];

describe("computeWatchStatsFromMovies", () => {
  it("matches the current stats contract", () => {
    expect(computeWatchStatsFromMovies(WATCHED_MOVIES)).toEqual({
      total: 2,
      avgAdam: 7,
      avgSean: 8,
      totalHours: 3.5,
      topGenre: "Drama",
      adamSuggestedWatched: 1,
      seanSuggestedWatched: 1,
    });
  });

  it("returns the empty-state stats object when no watched movies exist", () => {
    expect(computeWatchStatsFromMovies([])).toEqual({
      total: 0,
      avgAdam: 0,
      avgSean: 0,
      totalHours: 0,
      topGenre: "N/A",
      adamSuggestedWatched: 0,
      seanSuggestedWatched: 0,
    });
  });
});
