import { WatchLogView } from "@/components/WatchLogView";
import { getWatchStats, getWatchedMovies } from "@/lib/movies";

export const metadata = {
  title: "Log",
};

export default async function LogPage() {
  const [watched, stats] = await Promise.all([getWatchedMovies(), getWatchStats()]);
  return <WatchLogView stats={stats} watched={watched} />;
}
