import { readFileSync } from "node:fs";

const BRACKET_PASSWORD_RE = /(postgresql?:\/\/[^:]+:)\[([^\]]+)\](@)/;
let cachedSecrets: Record<string, string> | null = null;

function readLocalSecrets() {
  if (cachedSecrets) {
    return cachedSecrets;
  }

  try {
    const text = readFileSync(".streamlit/secrets.toml", "utf8");
    const values: Record<string, string> = {};
    for (const key of ["DATABASE_URL", "TMDB_READ_TOKEN", "TMDB_API_KEY"]) {
      const match = text.match(new RegExp(`^\\s*${key}\\s*=\\s*"([^"]*)"`, "m"));
      if (match?.[1]) {
        values[key] = match[1].trim();
      }
    }
    cachedSecrets = values;
    return values;
  } catch {
    cachedSecrets = {};
    return cachedSecrets;
  }
}

function requireEnv(name: string) {
  const value = process.env[name]?.trim() || readLocalSecrets()[name]?.trim();
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export function normalizeDatabaseUrl(url: string) {
  let normalized = url.trim();
  if (normalized.startsWith("postgres://")) {
    normalized = normalized.replace("postgres://", "postgresql://");
  }
  if (BRACKET_PASSWORD_RE.test(normalized)) {
    normalized = normalized.replace(BRACKET_PASSWORD_RE, "$1$2$3");
  }
  return normalized;
}

export function getDatabaseUrl() {
  return normalizeDatabaseUrl(requireEnv("DATABASE_URL"));
}

export function getTmdbCredentials() {
  const localSecrets = readLocalSecrets();
  const readToken = process.env.TMDB_READ_TOKEN?.trim() || localSecrets.TMDB_READ_TOKEN?.trim() || "";
  const apiKey = process.env.TMDB_API_KEY?.trim() || localSecrets.TMDB_API_KEY?.trim() || "";

  if (!readToken && !apiKey) {
    throw new Error(
      "TMDB credentials are missing. Add TMDB_READ_TOKEN or TMDB_API_KEY to your environment.",
    );
  }

  return { readToken, apiKey };
}
