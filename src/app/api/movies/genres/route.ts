import { NextResponse } from "next/server";
import { getAllGenres } from "@/lib/movies";
import { jsonError } from "@/lib/api";

export async function GET() {
  try {
    const genres = await getAllGenres();
    return NextResponse.json({ genres });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not load genres.", 500);
  }
}
