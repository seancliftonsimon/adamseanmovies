"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "@/lib/constants";

type PrimaryNavProps = {
  variant: "top" | "bottom";
};

export function PrimaryNav({ variant }: PrimaryNavProps) {
  const pathname = usePathname();
  const isBottom = variant === "bottom";

  return (
    <nav className={isBottom ? "bottom-nav" : "nav-row"} aria-label="Primary navigation">
      {NAV_ITEMS.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={isBottom ? "bottom-nav__link" : "nav-link"}
            data-active={isActive}
          >
            <span aria-hidden>{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
