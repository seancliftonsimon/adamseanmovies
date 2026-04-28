import type { MovieListType } from "@/lib/types";

export const APP_NAME = "Adam & Sean Movie Night";
export const MAX_MOVIES = 20_000;
export const MAX_OVERVIEW_CHARS = 2_000;
export const MAX_NOTES_CHARS = 2_000;

export const LIST_TYPE_LABELS: Record<MovieListType, string> = {
  adam_pick: "Adam's Picks",
  sean_pick: "Sean's Picks",
  mutual: "Mutual Discoveries",
};

export const LIST_TYPE_SHORT_LABELS: Record<MovieListType, string> = {
  adam_pick: "Adam",
  sean_pick: "Sean",
  mutual: "Shared",
};

export const LIST_TYPE_ADDED_BY: Record<MovieListType, string> = {
  adam_pick: "Adam",
  sean_pick: "Sean",
  mutual: "Both",
};

export const NAV_ITEMS = [
  { href: "/add", label: "Add", icon: "🎬" },
  { href: "/pick", label: "Pick", icon: "🎰" },
  { href: "/lists", label: "Lists", icon: "📋" },
  { href: "/log", label: "Log", icon: "📼" },
] as const;

export const PICK_LIST_FILTERS = [
  { label: "All", value: "all" },
  { label: "Adam's Picks", value: "adam_pick" },
  { label: "Sean's Picks", value: "sean_pick" },
  { label: "Mutual Discoveries", value: "mutual" },
] as const;

export const RUNTIME_PRESETS = [
  { label: "Any Length", value: "any", maxMinutes: null },
  { label: "Under 1h 30m", value: "90", maxMinutes: 90 },
  { label: "Under 2h", value: "120", maxMinutes: 120 },
  { label: "Under 2h 30m", value: "150", maxMinutes: 150 },
  { label: "Custom", value: "custom", maxMinutes: null },
] as const;

export const SHELF_SORT_OPTIONS = [
  "Recently Added",
  "Title A-Z",
  "Shortest First",
  "Longest First",
] as const;

export const WATCH_LOG_VIEWS = ["Overview", "Watched Shelf"] as const;

export const POSTER_PLACEHOLDER_SRC = "/poster-placeholder.svg";
