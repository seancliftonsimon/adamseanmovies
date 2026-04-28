import Image from "next/image";
import { POSTER_PLACEHOLDER_SRC } from "@/lib/constants";
import { getPosterUrl } from "@/lib/posters";

type PosterProps = {
  posterPath: string | null | undefined;
  title: string;
  size?: string;
  variant?: "frame" | "thumb";
  priority?: boolean;
};

export function Poster({
  posterPath,
  title,
  size = "w500",
  variant = "frame",
  priority = false,
}: PosterProps) {
  const src = getPosterUrl(posterPath, size) ?? POSTER_PLACEHOLDER_SRC;

  return (
    <div className={variant === "frame" ? "poster-frame" : "poster-thumb"}>
      <Image
        alt={`Poster for ${title}`}
        className="poster-image"
        height={variant === "frame" ? 750 : 278}
        priority={priority}
        src={src}
        width={variant === "frame" ? 500 : 185}
      />
    </div>
  );
}
