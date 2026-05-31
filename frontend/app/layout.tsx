import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "splat3D",
  description: "Upload a short video and generate a 3D Gaussian Splat.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
