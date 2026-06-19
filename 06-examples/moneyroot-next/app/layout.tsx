import type { Metadata } from "next";
import { AgentationDevToolbar } from "./components/AgentationDevToolbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "머니루트 강의",
  description: "머니루트 강의 목록형 랜딩 페이지",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>
        {children}
        <AgentationDevToolbar />
      </body>
    </html>
  );
}
