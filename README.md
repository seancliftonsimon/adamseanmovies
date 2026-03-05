# Adam & Sean Movie Night

A couples movie watchlist app built with Streamlit. Search for movies, organize them into lists, randomly pick what to watch, and keep a log of everything you've seen together.

## Features

- **Add a Movie** — Search TMDb, preview full details (poster, director, genres, runtime), and add to one of three lists:
  - Adam's Picks (movies Adam has seen and wants to share)
  - Sean's Picks (movies Sean has seen and wants to share)
  - Mutual Discoveries (neither has seen — both want to)
- **Pick for Us** — Randomly select a movie with a slot-machine-style reveal animation. Filter by whose picks, genre, runtime, or quick "vibe" presets.
- **Our Lists** — Browse all unwatched movies, sorted and organized by list type.
- **Watch Log** — Track watched movies with individual ratings, notes, and fun stats.

## Setup

1. **Get TMDb credentials** at [themoviedb.org](https://www.themoviedb.org/settings/api)

2. **Create** `.streamlit/secrets.toml` with either a read token, an API key, or both:
   ```toml
   TMDB_READ_TOKEN = "your_read_access_token"
   TMDB_API_KEY = "your_api_key"
   ```

3. **Create a Supabase Postgres project** (recommended for shared persistent data):
   - In Supabase, copy the connection string from:
     - **Connect** -> **Pooler** -> **Connection string** -> **URI**
   - For Streamlit Cloud, prefer the **Pooler URI** (IPv4 compatible).
   - Ensure it includes SSL (`sslmode=require`), for example:
     ```toml
     DATABASE_URL = "postgresql://postgres.[YOUR_PROJECT_REF]:[YOUR_PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require"
     ```
   - Add that `DATABASE_URL` to Streamlit secrets in local and deployed environments.
   - On startup, the app will auto-create the `movies` table and indexes if they do not exist.

4. **Install dependencies and run:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

### Database behavior

- If `DATABASE_URL` is set, the app uses Postgres (Supabase), giving one shared dataset for all users.
- If `DATABASE_URL` is not set, the app falls back to local SQLite (`movies.db`) for local development.

## Tech Stack

- **Streamlit** — UI framework
- **TMDb API** — Movie data, posters, credits (free)
- **Supabase Postgres** — Shared persistent multi-user database
- **SQLite** — Local fallback database (zero config)
