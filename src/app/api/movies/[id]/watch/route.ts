import { NextResponse } from "next/server";
import { markMovieWatched } from "@/lib/movies";
import { jsonError } from "@/lib/api";
import { watchPayloadSchema } from "@/lib/validation";

export async function PATCH(
  request: Request,
  context: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await context.params;
    const movieId = Number.parseInt(id, 10);
    if (!Number.isFinite(movieId)) {
      return jsonError("Invalid movie id.");
    }

    const payload = watchPayloadSchema.parse(await request.json());
    const movie = await markMovieWatched(movieId, payload);
    return NextResponse.json({ movie });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not update movie.", 500);
  }
}
