import type { Metadata } from "next";
import { productConfig } from "../config/product";
import "./globals.css";

export const metadata: Metadata = {
  title: productConfig.name,
  description: productConfig.description,
  icons: {
    icon: "/icon.svg",
    shortcut: "/icon.svg",
    apple: "/canon-logo.svg"
  }
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
