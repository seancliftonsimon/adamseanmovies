import "server-only";

import { getTmdbCredentials } from "@/lib/env";
import type { MovieDetails, MovieSearchResult } from "@/lib/types";

const BASE_URL = "https://api.themoviedb.org/3";

function getAuthConfig() {
  const { readToken, apiKey } = getTmdbCredentials();
  const headers: Record<string, string> = {
    accept: "application/json",
  };

  if (readToken) {
    headers.Authorization = `Bearer ${readToken}`;
    return {
      headers,
      baseParams: {},
    };
  }

  return {
    headers,
    baseParams: {
      api_key: apiKey,
    },
  };
}

async function requestTmdb(path: string, params?: Record<string, string | number | boolean>) {
  const auth = getAuthConfig();
  const search = new URLSearchParams();

  for (const [key, value] of Object.entries(auth.baseParams)) {
    search.set(key, String(value));
  }

  for (const [key, value] of Object.entries(params ?? {})) {
    search.set(key, String(value));
  }

  const response = await fetch(`${BASE_URL}${path}?${search.toString()}`, {
    headers: auth.headers,
    next: { revalidate: 60 * 60 * 24 },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("TMDb auth failed (401). Verify TMDB_READ_TOKEN or TMDB_API_KEY.");
    }
    throw new Error(`TMDb request failed with status ${response.status}`);
  }

  return response.json();
}

export async function searchTmdbMovies(query: string, page = 1, year?: number | null) {
  const data = await requestTmdb("/search/movie", {
    query,
    page,
    include_adult: false,
    ...(year ? { primary_release_year: year } : {}),
  });

  const results: MovieSearchResult[] = Array.isArray(data.results)
    ? data.results.map((result: Record<string, unknown>) => ({
        id: Number(result.id),
        title: String(result.title ?? "Unknown"),
        releaseDate: typeof result.release_date === "string" ? result.release_date : null,
        overview: typeof result.overview === "string" ? result.overview : null,
        posterPath: typeof result.poster_path === "string" ? result.poster_path : null,
      }))
    : [];

  return {
    results,
    totalResults: Number(data.total_results ?? 0),
  };
}

export async function getTmdbMovieDetails(tmdbId: number): Promise<MovieDetails> {
  const data = await requestTmdb(`/movie/${tmdbId}`, {
    append_to_response: "credits",
  });

  let director = "";
  const crew = Array.isArray(data?.credits?.crew) ? data.credits.crew : [];
  for (const member of crew) {
    if (member?.job === "Director" && typeof member?.name === "string") {
      director = member.name;
      break;
    }
  }

  const genres = Array.isArray(data.genres)
    ? data.genres
        .map((genre: Record<string, unknown>) =>
          typeof genre.name === "string" ? genre.name : null,
        )
        .filter((genre: string | null): genre is string => Boolean(genre))
    : [];

  const releaseDate = typeof data.release_date === "string" ? data.release_date : "";
  const year = releaseDate ? Number.parseInt(releaseDate.slice(0, 4), 10) || null : null;

  return {
    tmdbId: Number(data.id),
    title: String(data.title ?? "Unknown"),
    year,
    posterPath: typeof data.poster_path === "string" ? data.poster_path : null,
    director,
    genres,
    runtime: typeof data.runtime === "number" ? data.runtime : null,
    overview: typeof data.overview === "string" ? data.overview : "",
    voteAverage: typeof data.vote_average === "number" ? data.vote_average : 0,
  };
}
