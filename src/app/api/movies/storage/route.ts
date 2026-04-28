import { NextResponse } from "next/server";
import { getStorageGuardrailStatus } from "@/lib/movies";
import { jsonError } from "@/lib/api";

export async function GET() {
  try {
    const storage = await getStorageGuardrailStatus();
    return NextResponse.json({ storage });
  } catch (error) {
    return jsonError(error instanceof Error ? error.message : "Could not load storage.", 500);
  }
}
