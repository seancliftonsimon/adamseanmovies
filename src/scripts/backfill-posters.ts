import { getMoviesMissingPosters, updateMovieMetadata } from "@/lib/movies";
import { getTmdbMovieDetails, searchTmdbMovies } from "@/lib/tmdb";

const YEAR_RE = /\s*\((\d{4})\)\s*$/;

async function main() {
  const missing = await getMoviesMissingPosters();
  let updated = 0;
  let skipped = 0;

  for (const movie of missing) {
    const match = YEAR_RE.exec(movie.title);
    const searchTitle = match ? movie.title.slice(0, match.index).trim() : movie.title;
    const year = match ? Number.parseInt(match[1], 10) : undefined;

    try {
      let { results } = await searchTmdbMovies(searchTitle, 1, year);
      if (!results.length && year) {
        ({ results } = await searchTmdbMovies(searchTitle));
      }
      if (!results.length) {
        skipped += 1;
        console.log(`Skipped ${movie.title}: no TMDb match.`);
        continue;
      }

      const top =
        year != null
          ? results.find((result) => result.releaseDate?.slice(0, 4) === String(year)) ?? results[0]
          : results[0];

      const details = await getTmdbMovieDetails(top.id);
      await updateMovieMetadata(movie.id, details);
      updated += 1;
      console.log(`Updated ${movie.title}`);
    } catch (error) {
      skipped += 1;
      console.log(`Skipped ${movie.title}: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  console.log(`Poster backfill complete. Updated: ${updated}. Skipped: ${skipped}.`);
}

main().catch((error) => {
  console.error("Poster backfill failed:", error);
  process.exitCode = 1;
});
