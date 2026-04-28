import { NextResponse } from "next/server";
import { getTmdbMovieDetails } from "@/lib/tmdb";
import { jsonError } from "@/lib/api";

export async function GET(
  _request: Request,
  context: { params: Promise<{ tmdbId: string }> },
) {
  try {
    const { tmdbId } = await context.params;
    const id = Number.parseInt(tmdbId, 10);
    if (!Number.isFinite(id)) {
      return jsonError("Invalid TMDb id.");
    }

    const movie = await getTmdbMovieDetails(id);
    return NextResponse.json({ movie });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not load TMDb details.", 500);
  }
}
