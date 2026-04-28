import { LIST_TYPE_LABELS } from "@/lib/constants";
import type { MovieListType } from "@/lib/types";

export function parseGenres(value: string | null | undefined) {
  if (!value) {
    return [];
  }

  try {
    const parsed = JSON.parse(value);
    return Array.isArray(parsed) ? parsed.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}

export function serializeGenres(value: string[] | string | null | undefined) {
  if (!value) {
    return null;
  }
  if (typeof value === "string") {
    return value;
  }
  return JSON.stringify(value);
}

export function sanitizeText(value: string | null | undefined, maxChars: number) {
  if (value == null) {
    return null;
  }
  const trimmed = value.trim();
  if (!trimmed) {
    return "";
  }
  return trimmed.slice(0, maxChars);
}

export function formatRuntime(minutes: number | null | undefined) {
  if (!minutes) {
    return "Unknown";
  }
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (!hours) {
    return `${remainder}m`;
  }
  return `${hours}h ${remainder}m`;
}

export function formatRuntimeCompact(minutes: number) {
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (hours && remainder) {
    return `${hours}h ${String(remainder).padStart(2, "0")}m`;
  }
  if (hours) {
    return `${hours}h`;
  }
  return `${remainder}m`;
}

export function formatListLabel(listType: MovieListType) {
  return LIST_TYPE_LABELS[listType];
}

export function truncateText(value: string | null | undefined, maxChars: number) {
  if (!value) {
    return "";
  }
  return value.length > maxChars ? `${value.slice(0, maxChars)}...` : value;
}

export function formatDate(value: string | null | undefined) {
  if (!value) {
    return "Unknown date";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date);
}

export function sortByTitle<T extends { title: string }>(items: T[]) {
  return [...items].sort((a, b) => a.title.localeCompare(b.title));
}

export function ratingToStars(rating: number | null | undefined, maxStars = 10) {
  if (!rating) {
    return "Not rated";
  }
  const full = Math.floor(rating);
  const half = rating - full >= 0.5 ? 1 : 0;
  const empty = maxStars - full - half;
  return `${"★".repeat(full)}${half ? "½" : ""}${"☆".repeat(Math.max(0, empty))} ${rating}/10`;
}
