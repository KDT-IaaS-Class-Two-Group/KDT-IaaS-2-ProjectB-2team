import React from "react";
import { useRouter } from "next/router";
import Image from "next/image";

const MainPage: React.FC = () => {
  const router = useRouter();

  const handleStartClick = () => {
    router.push("/userpage");
  };

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center">
      {/* 이미지 영역 */}
      <div className="relative w-full max-w-[600px] h-3/4 flex items-center justify-center">
        <Image
          src="/images/Title.png"
          alt="Title"
          width={500}  // 이미지 너비
          height={300} // 이미지 높이
          style={{ objectFit: "contain" }}
          priority
        />
      </div>

      {/* 버튼 영역 */}
      <div className="w-2/5 flex justify-end">
        <button
          onClick={handleStartClick}
          className="px-5 py-3 bg-[#332F47CC] rounded border border-[#D9C4B2]
                     font-cfont text-lg text-[#C5C1C3] hover:bg-[#D9C4B2CC] hover:text-black">
          게임 시작
        </button>
      </div>
    </div>
  );
};

export default MainPage;