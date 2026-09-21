import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Quantum Ready Academy",
  description: "A video course on quantum readiness, from the book.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
