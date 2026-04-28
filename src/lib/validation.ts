import { z } from "zod";

export const movieListTypeSchema = z.enum(["adam_pick", "sean_pick", "mutual"]);

export const addMovieSchema = z.object({
  tmdbId: z.number().int().positive(),
  listType: movieListTypeSchema,
});

export const watchPayloadSchema = z.object({
  adamRating: z.number().min(1).max(10),
  seanRating: z.number().min(1).max(10),
  notes: z.string().optional(),
  watchedDate: z.string().min(1),
});
