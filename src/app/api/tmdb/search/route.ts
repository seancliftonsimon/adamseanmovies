import { NextRequest, NextResponse } from "next/server";
import { searchTmdbMovies } from "@/lib/tmdb";
import { jsonError } from "@/lib/api";

export async function GET(request: NextRequest) {
  try {
    const query = request.nextUrl.searchParams.get("query")?.trim() ?? "";
    const page = Number.parseInt(request.nextUrl.searchParams.get("page") ?? "1", 10);
    const yearRaw = request.nextUrl.searchParams.get("year");
    const year = yearRaw ? Number.parseInt(yearRaw, 10) : undefined;

    if (!query) {
      return jsonError("A search query is required.");
    }

    const data = await searchTmdbMovies(query, Number.isFinite(page) ? page : 1, year);
    return NextResponse.json(data);
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not search TMDb.", 500);
  }
}
