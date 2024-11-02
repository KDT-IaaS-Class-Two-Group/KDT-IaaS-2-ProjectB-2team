"use client";
import React, { useState, useEffect } from "react";
import { AppProps } from "next/app";
import { UserProvider } from "@/components/context";
import "../../public/globals.css";

const App: React.FC<AppProps> = ({ Component, pageProps }) => {
  const [isSmallViewport, setIsSmallViewport] = useState(false);

  // Threshold 설정 (예: 768px 이하일 때)
  const THRESHOLD_WIDTH = 768;

  useEffect(() => {
    // 뷰포트 크기 확인 함수
    const handleResize = () => {
      setIsSmallViewport(window.innerWidth <= THRESHOLD_WIDTH);
    };

    // 초기 뷰포트 크기 설정
    handleResize();
    
    // 리사이즈 이벤트 리스너 등록
    window.addEventListener("resize", handleResize);
    
    // 컴포넌트 언마운트 시 리스너 제거
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <UserProvider>
      <div className="relative w-screen h-screen">
        <div
          className={`absolute inset-0 bg-center bg-no-repeat ${
            isSmallViewport ? "bg-auto" : "bg-contain"
          }`}
          style={{
            backgroundImage: "url('/images/baseImage.png')",
          }}
        />
        <Component {...pageProps} />
      </div>
    </UserProvider>
  );
};

export default App;