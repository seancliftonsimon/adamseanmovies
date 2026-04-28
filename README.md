# Adam & Sean Movie Night

A mobile-first Next.js PWA for adding movies, picking something to watch together, browsing shared shelves, and keeping a watch log.

## Environment

Keep the current secret names:

```bash
DATABASE_URL=postgresql://...
TMDB_READ_TOKEN=...
TMDB_API_KEY=...
```

`TMDB_READ_TOKEN` is preferred. `TMDB_API_KEY` is only used as the fallback.

The app will use regular environment variables first. For local development, it also falls back to `.streamlit/secrets.toml` if those values already live there.

## Local Development

Install dependencies and start the app:

```bash
npm install
npm run dev
```

Then open [http://localhost:3000/add](http://localhost:3000/add).

## Scripts

- `npm run dev` — start the local Next.js app
- `npm run lint` — run ESLint
- `npm test` — run Vitest unit tests
- `npm run test:e2e` — run the Playwright smoke test
- `npm run build` — production build check
- `npm run db:seed` — seed a small starter dataset into an empty database
- `npm run db:backfill-posters` — backfill missing poster metadata from TMDb

## Notes

- The app preserves the existing `movies` table shape and `list_type` values: `adam_pick`, `sean_pick`, `mutual`.
- Hidden Streamlit side effects were moved into explicit scripts:
  - seeding is no longer automatic
  - poster backfill is no longer tied to page load
- The app is designed for Vercel + Neon and keeps TMDb credentials server-side.
- It preserves the current `movies` table contract so it can point at the existing Neon database immediately.

## Deployment

Deploy the repo root as the Vercel project and add the same env var names there. If your Neon connection string needs a pooled/serverless endpoint, update the value of `DATABASE_URL` without renaming the key.
