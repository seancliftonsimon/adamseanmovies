export type MovieListType = "adam_pick" | "sean_pick" | "mutual";

export type MovieRecord = {
  id: number;
  tmdbId: number | null;
  title: string;
  year: number | null;
  posterPath: string | null;
  director: string | null;
  genres: string | null;
  genresList: string[];
  runtime: number | null;
  overview: string | null;
  listType: MovieListType;
  addedBy: string;
  addedDate: string | null;
  watched: boolean;
  watchedDate: string | null;
  adamRating: number | null;
  seanRating: number | null;
  notes: string | null;
};

export type MovieInsertInput = {
  tmdbId: number | null;
  title: string;
  year: number | null;
  posterPath: string | null;
  director: string | null;
  genres: string[] | string | null;
  runtime: number | null;
  overview: string | null;
  listType: MovieListType;
  addedBy: string;
  watched?: boolean;
  watchedDate?: string | null;
  adamRating?: number | null;
  seanRating?: number | null;
  notes?: string | null;
};

export type WatchPayload = {
  adamRating: number;
  seanRating: number;
  notes?: string;
  watchedDate: string;
};

export type WatchStats = {
  total: number;
  avgAdam: number;
  avgSean: number;
  totalHours: number;
  topGenre: string;
  adamSuggestedWatched: number;
  seanSuggestedWatched: number;
};

export type StorageStatus = {
  count: number;
  maxMovies: number;
  percentUsed: number;
};

export type DbStatus = {
  backend: "postgres";
  connected: boolean;
  detail: string;
  fallback: false;
};

export type MovieSearchResult = {
  id: number;
  title: string;
  releaseDate: string | null;
  overview: string | null;
  posterPath: string | null;
};

export type MovieDetails = {
  tmdbId: number;
  title: string;
  year: number | null;
  posterPath: string | null;
  director: string;
  genres: string[];
  runtime: number | null;
  overview: string;
  voteAverage: number;
};
