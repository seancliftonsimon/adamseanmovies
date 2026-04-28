import { NextResponse } from "next/server";
import { getWatchStats } from "@/lib/movies";
import { jsonError } from "@/lib/api";

export async function GET() {
  try {
    const stats = await getWatchStats();
    return NextResponse.json({ stats });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not load stats.", 500);
  }
}
