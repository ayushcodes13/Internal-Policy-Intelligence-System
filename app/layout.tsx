import type { Metadata } from "next";
import { productConfig } from "../config/product";
import "./globals.css";

export const metadata: Metadata = {
  title: productConfig.name,
  description: productConfig.description
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
