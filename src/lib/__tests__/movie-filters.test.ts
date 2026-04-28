import { describe, expect, it } from "vitest";
import { buildActivePickFilters, filterPickMovies, sortShelfMovies } from "@/lib/movie-filters";
import type { MovieRecord } from "@/lib/types";

const MOVIES: MovieRecord[] = [
  {
    id: 1,
    tmdbId: 1,
    title: "Short Drama",
    year: 2000,
    posterPath: null,
    director: null,
    genres: '["Drama"]',
    genresList: ["Drama"],
    runtime: 90,
    overview: null,
    listType: "adam_pick",
    addedBy: "Adam",
    addedDate: "2025-01-01T00:00:00Z",
    watched: false,
    watchedDate: null,
    adamRating: null,
    seanRating: null,
    notes: null,
  },
  {
    id: 2,
    tmdbId: 2,
    title: "Long Comedy",
    year: 2001,
    posterPath: null,
    director: null,
    genres: '["Comedy"]',
    genresList: ["Comedy"],
    runtime: 150,
    overview: null,
    listType: "sean_pick",
    addedBy: "Sean",
    addedDate: "2025-01-02T00:00:00Z",
    watched: false,
    watchedDate: null,
    adamRating: null,
    seanRating: null,
    notes: null,
  },
  {
    id: 3,
    tmdbId: 3,
    title: "Mystery Unknown Runtime",
    year: 2002,
    posterPath: null,
    director: null,
    genres: '["Mystery"]',
    genresList: ["Mystery"],
    runtime: null,
    overview: null,
    listType: "mutual",
    addedBy: "Both",
    addedDate: "2025-01-03T00:00:00Z",
    watched: false,
    watchedDate: null,
    adamRating: null,
    seanRating: null,
    notes: null,
  },
];

describe("filterPickMovies", () => {
  it("uses OR logic for multi-genre filters", () => {
    const filtered = filterPickMovies(MOVIES, {
      listFilter: "all",
      selectedGenres: ["Drama", "Comedy"],
      runtimeFilter: "any",
      customRuntime: 150,
    });

    expect(filtered.map((movie) => movie.id)).toEqual([1, 2]);
  });

  it("allows unknown runtime movies through runtime filters", () => {
    const filtered = filterPickMovies(MOVIES, {
      listFilter: "all",
      selectedGenres: [],
      runtimeFilter: "120",
      customRuntime: 120,
    });

    expect(filtered.map((movie) => movie.id)).toEqual([1, 3]);
  });
});

describe("buildActivePickFilters", () => {
  it("formats custom runtime labels", () => {
    expect(
      buildActivePickFilters({
        listFilter: "adam_pick",
        selectedGenres: ["Drama"],
        runtimeFilter: "custom",
        customRuntime: 150,
      }),
    ).toEqual(["Adam's Picks", "Drama", "Under 2h 30m"]);
  });
});

describe("sortShelfMovies", () => {
  it("keeps missing runtimes last for shortest-first sorting", () => {
    const sorted = sortShelfMovies(MOVIES, "Shortest First");
    expect(sorted.map((movie) => movie.id)).toEqual([1, 2, 3]);
  });

  it("keeps missing runtimes last for longest-first sorting", () => {
    const sorted = sortShelfMovies(MOVIES, "Longest First");
    expect(sorted.map((movie) => movie.id)).toEqual([2, 1, 3]);
  });
});
