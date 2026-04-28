import "server-only";

import { neon } from "@neondatabase/serverless";
import { unstable_noStore as noStore } from "next/cache";
import {
  LIST_TYPE_ADDED_BY,
  MAX_MOVIES,
  MAX_NOTES_CHARS,
  MAX_OVERVIEW_CHARS,
} from "@/lib/constants";
import { getDatabaseUrl } from "@/lib/env";
import type {
  DbStatus,
  MovieDetails,
  MovieInsertInput,
  MovieListType,
  MovieRecord,
  StorageStatus,
  WatchPayload,
} from "@/lib/types";
import { parseGenres, sanitizeText, serializeGenres } from "@/lib/utils";
import { computeWatchStatsFromMovies } from "@/lib/watch-stats";

type DbMovieRow = {
  id: number;
  tmdb_id: number | null;
  title: string;
  year: number | null;
  poster_path: string | null;
  director: string | null;
  genres: string | null;
  runtime: number | null;
  overview: string | null;
  list_type: MovieListType;
  added_by: string;
  added_date: string | Date | null;
  watched: boolean;
  watched_date: string | Date | null;
  adam_rating: number | null;
  sean_rating: number | null;
  notes: string | null;
};

type DuplicateError = Error & { code?: string };

let schemaReady: Promise<void> | null = null;

function getSql() {
  return neon(getDatabaseUrl());
}

async function ensureSchema() {
  if (!schemaReady) {
    schemaReady = (async () => {
      const sql = getSql();
      await sql`
        CREATE TABLE IF NOT EXISTS movies (
          id BIGSERIAL PRIMARY KEY,
          tmdb_id BIGINT UNIQUE,
          title TEXT NOT NULL,
          year INTEGER,
          poster_path TEXT,
          director TEXT,
          genres TEXT,
          runtime INTEGER,
          overview TEXT,
          list_type TEXT NOT NULL,
          added_by TEXT NOT NULL,
          added_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
          watched BOOLEAN DEFAULT FALSE,
          watched_date DATE,
          adam_rating DOUBLE PRECISION,
          sean_rating DOUBLE PRECISION,
          notes TEXT
        )
      `;
      await sql`
        CREATE INDEX IF NOT EXISTS idx_movies_watched_list_added_date
        ON movies (watched, list_type, added_date DESC)
      `;
      await sql`
        CREATE INDEX IF NOT EXISTS idx_movies_watched_watched_date
        ON movies (watched, watched_date DESC)
      `;
    })();
  }

  await schemaReady;
}

function toIsoString(value: string | Date | null) {
  if (!value) {
    return null;
  }
  if (typeof value === "string") {
    return value;
  }
  return value.toISOString();
}

function mapRow(row: DbMovieRow): MovieRecord {
  return {
    id: row.id,
    tmdbId: row.tmdb_id,
    title: row.title,
    year: row.year,
    posterPath: row.poster_path,
    director: row.director,
    genres: row.genres,
    genresList: parseGenres(row.genres),
    runtime: row.runtime,
    overview: row.overview,
    listType: row.list_type,
    addedBy: row.added_by,
    addedDate: toIsoString(row.added_date),
    watched: Boolean(row.watched),
    watchedDate: toIsoString(row.watched_date),
    adamRating: row.adam_rating,
    seanRating: row.sean_rating,
    notes: row.notes,
  };
}

function isDuplicateError(error: unknown): error is DuplicateError {
  if (!(error instanceof Error)) {
    return false;
  }
  const duplicate = error as DuplicateError;
  return duplicate.code === "23505" || /duplicate key/i.test(duplicate.message);
}

async function countMovies() {
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`SELECT COUNT(*)::int AS c FROM movies`) as { c: number }[];
  return rows[0]?.c ?? 0;
}

function todayIsoDate() {
  return new Date().toISOString().slice(0, 10);
}

export function toAddedBy(listType: MovieListType) {
  return LIST_TYPE_ADDED_BY[listType];
}

export async function getDbStatus(): Promise<DbStatus> {
  await ensureSchema();
  return {
    backend: "postgres",
    connected: true,
    detail: "connected",
    fallback: false,
  };
}

export async function getStorageGuardrailStatus(): Promise<StorageStatus> {
  noStore();
  const count = await countMovies();
  return {
    count,
    maxMovies: MAX_MOVIES,
    percentUsed: MAX_MOVIES ? (count / MAX_MOVIES) * 100 : 0,
  };
}

export async function getUnwatchedMovies(listType?: MovieListType | null) {
  noStore();
  await ensureSchema();
  const sql = getSql();

  const rows = (listType
    ? await sql`
        SELECT * FROM movies
        WHERE watched = FALSE AND list_type = ${listType}
        ORDER BY added_date DESC
      `
    : await sql`
        SELECT * FROM movies
        WHERE watched = FALSE
        ORDER BY added_date DESC
      `) as DbMovieRow[];

  return rows.map(mapRow);
}

export async function getWatchedMovies() {
  noStore();
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`
    SELECT * FROM movies
    WHERE watched = TRUE
    ORDER BY watched_date DESC, added_date DESC
  `) as DbMovieRow[];
  return rows.map(mapRow);
}

export async function movieExists(tmdbId: number) {
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`
    SELECT * FROM movies
    WHERE tmdb_id = ${tmdbId}
    LIMIT 1
  `) as DbMovieRow[];
  return rows[0] ? mapRow(rows[0]) : null;
}

export async function insertMovieRecord(input: MovieInsertInput) {
  await ensureSchema();
  const sql = getSql();

  if ((await countMovies()) >= MAX_MOVIES) {
    throw new Error(
      `Movie limit reached (${MAX_MOVIES}). Remove old entries before adding more.`,
    );
  }

  try {
    const rows = (await sql`
      INSERT INTO movies (
        tmdb_id,
        title,
        year,
        poster_path,
        director,
        genres,
        runtime,
        overview,
        list_type,
        added_by,
        watched,
        watched_date,
        adam_rating,
        sean_rating,
        notes
      )
      VALUES (
        ${input.tmdbId},
        ${input.title},
        ${input.year},
        ${input.posterPath},
        ${input.director},
        ${serializeGenres(input.genres)},
        ${input.runtime},
        ${sanitizeText(input.overview, MAX_OVERVIEW_CHARS)},
        ${input.listType},
        ${input.addedBy},
        ${input.watched ?? false},
        ${input.watchedDate ?? null},
        ${input.adamRating ?? null},
        ${input.seanRating ?? null},
        ${sanitizeText(input.notes, MAX_NOTES_CHARS)}
      )
      RETURNING *
    `) as DbMovieRow[];
    return { success: true, movie: mapRow(rows[0]) };
  } catch (error) {
    if (isDuplicateError(error)) {
      return { success: false, movie: null };
    }
    throw error;
  }
}

export async function addMovieFromDetails(details: MovieDetails, listType: MovieListType) {
  return insertMovieRecord({
    tmdbId: details.tmdbId,
    title: details.title,
    year: details.year,
    posterPath: details.posterPath,
    director: details.director,
    genres: details.genres,
    runtime: details.runtime,
    overview: details.overview,
    listType,
    addedBy: toAddedBy(listType),
  });
}

export async function markMovieWatched(movieId: number, payload: WatchPayload) {
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`
    UPDATE movies
    SET watched = TRUE,
        watched_date = ${payload.watchedDate || todayIsoDate()},
        adam_rating = ${payload.adamRating},
        sean_rating = ${payload.seanRating},
        notes = ${sanitizeText(payload.notes, MAX_NOTES_CHARS)}
    WHERE id = ${movieId}
    RETURNING *
  `) as DbMovieRow[];

  if (!rows[0]) {
    throw new Error("Movie not found.");
  }

  return mapRow(rows[0]);
}

export async function removeMovie(movieId: number) {
  await ensureSchema();
  const sql = getSql();
  await sql`DELETE FROM movies WHERE id = ${movieId}`;
}

export async function getMoviesMissingPosters() {
  await ensureSchema();
  const sql = getSql();
  return (await sql`
    SELECT id, title
    FROM movies
    WHERE (poster_path IS NULL OR poster_path = '')
      AND title IS NOT NULL
  `) as { id: number; title: string }[];
}

export async function updateMovieMetadata(movieId: number, details: MovieDetails) {
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`
    UPDATE movies
    SET
      tmdb_id = COALESCE(tmdb_id, ${details.tmdbId}),
      poster_path = COALESCE(poster_path, ${details.posterPath}),
      year = COALESCE(year, ${details.year}),
      director = COALESCE(director, ${details.director}),
      genres = COALESCE(genres, ${serializeGenres(details.genres)}),
      runtime = COALESCE(runtime, ${details.runtime}),
      overview = COALESCE(overview, ${sanitizeText(details.overview, MAX_OVERVIEW_CHARS)})
    WHERE id = ${movieId}
    RETURNING *
  `) as DbMovieRow[];
  return rows[0] ? mapRow(rows[0]) : null;
}

export async function getAllGenres() {
  noStore();
  await ensureSchema();
  const sql = getSql();
  const rows = (await sql`
    SELECT genres
    FROM movies
    WHERE watched = FALSE
  `) as { genres: string | null }[];

  const allGenres = new Set<string>();
  for (const row of rows) {
    for (const genre of parseGenres(row.genres)) {
      allGenres.add(genre);
    }
  }

  return [...allGenres].sort((a, b) => a.localeCompare(b));
}

export async function getWatchStats() {
  const watched = await getWatchedMovies();
  return computeWatchStatsFromMovies(watched);
}
