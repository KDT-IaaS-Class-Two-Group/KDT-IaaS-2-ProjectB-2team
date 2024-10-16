import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="/fonts/국립박물관문화재단클래식M.otf" // 여기에 커스텀 폰트 CSS 파일 경로를 설정하세요.
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
