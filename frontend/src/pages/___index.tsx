"use client";

import { ReactNode } from "react";
import '../app/globals.css';
import Link from "next/link";
// props의 타입을 정의합니다.
interface MainPageProps {
  children: ReactNode; // children의 타입을 ReactNode로 지정합니다.
}

export default function MainPage({ children }: MainPageProps) {
  return (
    <div id="root"
    className="m-64 w-3 h-3  border-slate-900">
      {children}
      <div>
        <Link
        href={"/test"}>test 페이지로 이동</Link>
      </div>
    </div>
  );
}
