const IMAGE_BASE = "https://image.tmdb.org/t/p";

export function getPosterUrl(posterPath: string | null | undefined, size = "w500") {
  if (!posterPath) {
    return null;
  }
  return `${IMAGE_BASE}/${size}${posterPath}`;
}
