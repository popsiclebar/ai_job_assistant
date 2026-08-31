/**
 * Defines shared document metadata, navigation, and page structure for every route.
 * Feature pages render inside this stable application shell.
 */
import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Job Assistant",
  description: "Local-first job discovery and application preparation",
};

const navigation = [
  ["Dashboard", "/"],
  ["Jobs", "/jobs"],
  ["Applications", "/applications"],
  ["Profile", "/profile"],
  ["Resume", "/resume"],
  ["Settings", "/settings"],
] as const;

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  /** Render the common HTML document and primary application navigation. */
  return (
    <html lang="en">
      <body>
        <header className="siteHeader">
          <Link className="brand" href="/">
            AI Job Assistant
          </Link>
          <nav aria-label="Main navigation">
            {navigation.map(([label, href]) => (
              <Link href={href} key={href}>
                {label}
              </Link>
            ))}
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
