import { describe, expect, it } from "vitest";
import { normalizeDatabaseUrl } from "@/lib/env";

describe("normalizeDatabaseUrl", () => {
  it("converts postgres:// URLs to postgresql://", () => {
    expect(normalizeDatabaseUrl("postgres://user:pass@example.com/db")).toBe(
      "postgresql://user:pass@example.com/db",
    );
  });

  it("strips square brackets from passwords", () => {
    expect(
      normalizeDatabaseUrl("postgresql://user:[secret-pass]@example.com/db?sslmode=require"),
    ).toBe("postgresql://user:secret-pass@example.com/db?sslmode=require");
  });
});
