import { LIST_TYPE_LABELS, RUNTIME_PRESETS } from "@/lib/constants";
import type { MovieListType, MovieRecord } from "@/lib/types";
import { formatRuntimeCompact } from "@/lib/utils";

export type PickListFilterValue = "all" | MovieListType;
export type ShelfSortOption = "Recently Added" | "Title A-Z" | "Shortest First" | "Longest First";

export function filterPickMovies(
  movies: MovieRecord[],
  options: {
    listFilter: PickListFilterValue;
    selectedGenres: string[];
    runtimeFilter: (typeof RUNTIME_PRESETS)[number]["value"];
    customRuntime: number;
  },
) {
  return movies.filter((movie) => {
    if (options.listFilter !== "all" && movie.listType !== options.listFilter) {
      return false;
    }
    if (
      options.selectedGenres.length > 0 &&
      !options.selectedGenres.some((genre) => movie.genresList.includes(genre))
    ) {
      return false;
    }
    if (options.runtimeFilter === "any") {
      return true;
    }
    const runtimeLimit =
      options.runtimeFilter === "custom"
        ? options.customRuntime
        : RUNTIME_PRESETS.find((preset) => preset.value === options.runtimeFilter)?.maxMinutes ?? null;
    if (!runtimeLimit) {
      return true;
    }
    return movie.runtime == null || movie.runtime <= runtimeLimit;
  });
}

export function buildActivePickFilters(options: {
  listFilter: PickListFilterValue;
  selectedGenres: string[];
  runtimeFilter: (typeof RUNTIME_PRESETS)[number]["value"];
  customRuntime: number;
}) {
  return [
    ...(options.listFilter !== "all" ? [LIST_TYPE_LABELS[options.listFilter]] : []),
    ...options.selectedGenres,
    ...(options.runtimeFilter === "custom"
      ? [`Under ${formatRuntimeCompact(options.customRuntime)}`]
      : options.runtimeFilter !== "any"
        ? [RUNTIME_PRESETS.find((preset) => preset.value === options.runtimeFilter)?.label ?? options.runtimeFilter]
        : []),
  ];
}

export function sortShelfMovies(movies: MovieRecord[], sortOption: ShelfSortOption) {
  if (sortOption === "Title A-Z") {
    return [...movies].sort((left, right) => left.title.localeCompare(right.title));
  }
  if (sortOption === "Shortest First") {
    return [...movies].sort((left, right) => (left.runtime ?? 9_999) - (right.runtime ?? 9_999));
  }
  if (sortOption === "Longest First") {
    return [...movies].sort((left, right) => (right.runtime ?? 0) - (left.runtime ?? 0));
  }
  return movies;
}
