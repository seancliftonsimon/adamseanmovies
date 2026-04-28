import type { MovieRecord, WatchStats } from "@/lib/types";

export function computeWatchStatsFromMovies(movies: MovieRecord[]): WatchStats {
  if (!movies.length) {
    return {
      total: 0,
      avgAdam: 0,
      avgSean: 0,
      totalHours: 0,
      topGenre: "N/A",
      adamSuggestedWatched: 0,
      seanSuggestedWatched: 0,
    };
  }

  const adamRatings = movies
    .map((movie) => movie.adamRating)
    .filter((rating): rating is number => typeof rating === "number");
  const seanRatings = movies
    .map((movie) => movie.seanRating)
    .filter((rating): rating is number => typeof rating === "number");
  const totalMinutes = movies.reduce((sum, movie) => sum + (movie.runtime ?? 0), 0);

  const genreCounts = new Map<string, number>();
  for (const movie of movies) {
    for (const genre of movie.genresList) {
      genreCounts.set(genre, (genreCounts.get(genre) ?? 0) + 1);
    }
  }

  let topGenre = "N/A";
  let topGenreCount = 0;
  for (const [genre, count] of genreCounts.entries()) {
    if (count > topGenreCount) {
      topGenre = genre;
      topGenreCount = count;
    }
  }

  return {
    total: movies.length,
    avgAdam: adamRatings.length
      ? Math.round((adamRatings.reduce((sum, rating) => sum + rating, 0) / adamRatings.length) * 10) /
        10
      : 0,
    avgSean: seanRatings.length
      ? Math.round((seanRatings.reduce((sum, rating) => sum + rating, 0) / seanRatings.length) * 10) /
        10
      : 0,
    totalHours: Math.round((totalMinutes / 60) * 10) / 10,
    topGenre,
    adamSuggestedWatched: movies.filter((movie) => movie.listType === "adam_pick").length,
    seanSuggestedWatched: movies.filter((movie) => movie.listType === "sean_pick").length,
  };
}
