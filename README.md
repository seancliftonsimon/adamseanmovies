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

1. **Get a free TMDb API key** at [themoviedb.org](https://www.themoviedb.org/settings/api)

2. **Create** `.streamlit/secrets.toml`:
   ```toml
   TMDB_API_KEY = "your_api_key"
   TMDB_READ_TOKEN = "your_read_access_token"
   ```

3. **Install dependencies and run:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Tech Stack

- **Streamlit** — UI framework
- **TMDb API** — Movie data, posters, credits (free)
- **SQLite** — Local database (zero config)
