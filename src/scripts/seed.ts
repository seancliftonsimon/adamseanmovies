import { getStorageGuardrailStatus, insertMovieRecord } from "@/lib/movies";
import type { MovieInsertInput } from "@/lib/types";

const STARTER_MOVIES: MovieInsertInput[] = [
  {
    tmdbId: 12614,
    title: "Victor/Victoria",
    year: 1982,
    posterPath: "/mCjXcPRM3Rc7gOCGeVrBdPvF2bk.jpg",
    director: "Blake Edwards",
    genres: ["Music", "Comedy", "Romance"],
    runtime: 134,
    overview:
      "A struggling female soprano finds work playing a male female impersonator, but it complicates her personal life.",
    listType: "adam_pick",
    addedBy: "Adam",
  },
  {
    tmdbId: 791177,
    title: "Bones and All",
    year: 2022,
    posterPath: "/dBQuk2LkHjrDsSjueirPQg96GCc.jpg",
    director: "Luca Guadagnino",
    genres: ["Horror", "Romance", "Drama"],
    runtime: 131,
    overview:
      "Abandoned by her father, a young woman embarks on a thousand-mile odyssey through the backroads of America.",
    listType: "adam_pick",
    addedBy: "Adam",
  },
  {
    tmdbId: 37233,
    title: "The Firm",
    year: 1993,
    posterPath: "/kFexXCzidkm4LwlgZqxsJsDQB5v.jpg",
    director: "Sydney Pollack",
    genres: ["Drama", "Mystery", "Thriller"],
    runtime: 154,
    overview:
      "Mitch McDeere is a young man with a promising future in Law and an offer that feels too good to refuse.",
    listType: "sean_pick",
    addedBy: "Sean",
  },
  {
    tmdbId: 290098,
    title: "The Handmaiden",
    year: 2016,
    posterPath: "/dLlH4aNHdnmf62umnInL8xPlPzw.jpg",
    director: "Park Chan-wook",
    genres: ["Thriller", "Drama", "Romance"],
    runtime: 145,
    overview:
      "1930s Korea, in the period of Japanese occupation, a new girl is hired as a handmaiden to a Japanese heiress.",
    listType: "sean_pick",
    addedBy: "Sean",
  },
  {
    tmdbId: 378,
    title: "Raising Arizona",
    year: 1987,
    posterPath: "/niKyjOqiB4XVl0BqgKTHIlHOCeF.jpg",
    director: "Joel Coen",
    genres: ["Comedy", "Crime"],
    runtime: 94,
    overview:
      "When a childless couple take one of a wealthy family's quintuplets, they must dodge the law and two bounty hunters.",
    listType: "mutual",
    addedBy: "Both",
  },
  {
    tmdbId: 279,
    title: "Amadeus",
    year: 1984,
    posterPath: "/gQRfiyfGvr1az0quaYyMram3Aqt.jpg",
    director: "Miloš Forman",
    genres: ["History", "Music", "Drama"],
    runtime: 160,
    overview:
      "Antonio Salieri becomes consumed by jealousy and resentment toward the youthful musical genius Wolfgang Amadeus Mozart.",
    listType: "mutual",
    addedBy: "Both",
  },
  {
    tmdbId: 76,
    title: "Before Sunrise",
    year: 1995,
    posterPath: "/kf1Jb1c2JAOqjuzA3H4oDM263uB.jpg",
    director: "Richard Linklater",
    genres: ["Drama", "Romance"],
    runtime: 101,
    overview:
      "An unexpected meeting on a train leads two travelers to spend an evening wandering the streets of Vienna.",
    listType: "sean_pick",
    addedBy: "Sean",
    watched: true,
    watchedDate: "2025-01-16",
    adamRating: 8,
    seanRating: 9,
    notes: "An all-timer for talking all night long.",
  },
  {
    tmdbId: 194,
    title: "Amélie",
    year: 2001,
    posterPath: "/nSxDa3M9aMvGVLoItzWTepQ5h5d.jpg",
    director: "Jean-Pierre Jeunet",
    genres: ["Comedy", "Romance"],
    runtime: 122,
    overview:
      "A shy Parisian waitress accidentally discovers a gift for helping others and decides to transform lives for the better.",
    listType: "sean_pick",
    addedBy: "Sean",
    watched: true,
    watchedDate: "2025-02-25",
    adamRating: 8,
    seanRating: 8,
  },
];

async function main() {
  const storage = await getStorageGuardrailStatus();
  if (storage.count > 0) {
    console.log(`Seed skipped: database already contains ${storage.count} movies.`);
    return;
  }

  for (const movie of STARTER_MOVIES) {
    await insertMovieRecord(movie);
    console.log(`Seeded ${movie.title}`);
  }

  console.log(`Seed complete: inserted ${STARTER_MOVIES.length} starter movies.`);
}

main().catch((error) => {
  console.error("Seed failed:", error);
  process.exitCode = 1;
});
