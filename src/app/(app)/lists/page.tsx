import { ListsView } from "@/components/ListsView";
import { getUnwatchedMovies } from "@/lib/movies";

export const metadata = {
  title: "Lists",
};

export default async function ListsPage() {
  const movies = await getUnwatchedMovies();
  return <ListsView initialMovies={movies} />;
}
