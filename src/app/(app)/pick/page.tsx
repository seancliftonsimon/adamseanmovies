import { PickView } from "@/components/PickView";
import { getAllGenres, getUnwatchedMovies } from "@/lib/movies";

export const metadata = {
  title: "Pick",
};

export default async function PickPage() {
  const [movies, genres] = await Promise.all([getUnwatchedMovies(), getAllGenres()]);
  return <PickView availableGenres={genres} initialMovies={movies} />;
}
