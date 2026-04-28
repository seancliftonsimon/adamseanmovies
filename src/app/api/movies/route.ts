import { NextRequest, NextResponse } from "next/server";
import { addMovieFromDetails, getUnwatchedMovies, getWatchedMovies, movieExists } from "@/lib/movies";
import { getTmdbMovieDetails } from "@/lib/tmdb";
import { jsonError } from "@/lib/api";
import { addMovieSchema, movieListTypeSchema } from "@/lib/validation";

export async function GET(request: NextRequest) {
  try {
    const status = request.nextUrl.searchParams.get("status");
    const listTypeRaw = request.nextUrl.searchParams.get("listType");
    const listType = listTypeRaw ? movieListTypeSchema.parse(listTypeRaw) : null;

    if (status === "watched") {
      const movies = await getWatchedMovies();
      return NextResponse.json({ movies });
    }

    const movies = await getUnwatchedMovies(listType);
    return NextResponse.json({ movies });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not load movies.", 500);
  }
}

export async function POST(request: NextRequest) {
  try {
    const payload = addMovieSchema.parse(await request.json());
    const existing = await movieExists(payload.tmdbId);

    if (existing) {
      return NextResponse.json({ existing }, { status: 409 });
    }

    const details = await getTmdbMovieDetails(payload.tmdbId);
    const result = await addMovieFromDetails(details, payload.listType);

    if (!result.success || !result.movie) {
      const existingMovie = await movieExists(payload.tmdbId);
      return NextResponse.json({ existing: existingMovie }, { status: 409 });
    }

    return NextResponse.json({ movie: result.movie }, { status: 201 });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not add movie.", 500);
  }
}
