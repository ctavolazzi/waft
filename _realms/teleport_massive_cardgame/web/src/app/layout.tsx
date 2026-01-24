import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Teleport Massive Card Game",
  description: "A collectible card game set in the quantum teleportation universe",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased min-h-screen`}>
        <Header />
        <main className="grid-bg min-h-[calc(100vh-73px)]">
          {children}
        </main>
      </body>
    </html>
  );
}
