import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Adam & Sean Movie Night",
    short_name: "Movie Night",
    description:
      "Add movies, pick something together, browse your lists, and keep a shared watch log.",
    start_url: "/add",
    display: "standalone",
    background_color: "#f7f3e8",
    theme_color: "#003399",
    orientation: "portrait",
    icons: [
      {
        src: "/icon?size=192",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/icon?size=512",
        sizes: "512x512",
        type: "image/png",
      },
      {
        src: "/apple-icon",
        sizes: "180x180",
        type: "image/png",
      },
    ],
  };
}
