import type { Metadata, Viewport } from "next";
import { Epilogue, Inter, Space_Grotesk } from "next/font/google";
import { ToastProvider } from "@/components/ToastProvider";
import { ServiceWorkerRegistrar } from "@/components/ServiceWorkerRegistrar";
import "./globals.css";

const displayFont = Epilogue({
  subsets: ["latin"],
  variable: "--font-display",
});

const bodyFont = Inter({
  subsets: ["latin"],
  variable: "--font-body",
});

const labelFont = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-label",
});

export const metadata: Metadata = {
  title: {
    default: "Adam & Sean Movie Night",
    template: "%s | Adam & Sean Movie Night",
  },
  description:
    "A mobile-first movie night app for adding, picking, organizing, and logging movies together.",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Adam & Sean",
  },
  formatDetection: {
    telephone: false,
  },
};

export const viewport: Viewport = {
  themeColor: "#003399",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${displayFont.variable} ${bodyFont.variable} ${labelFont.variable}`}
    >
      <body>
        <ToastProvider>
          <ServiceWorkerRegistrar />
          {children}
        </ToastProvider>
      </body>
    </html>
  );
}
