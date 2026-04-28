import { NextResponse } from "next/server";
import { removeMovie } from "@/lib/movies";
import { jsonError } from "@/lib/api";

export async function DELETE(
  _request: Request,
  context: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await context.params;
    const movieId = Number.parseInt(id, 10);
    if (!Number.isFinite(movieId)) {
      return jsonError("Invalid movie id.");
    }

    await removeMovie(movieId);
    return NextResponse.json({ ok: true });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not remove movie.", 500);
  }
}
