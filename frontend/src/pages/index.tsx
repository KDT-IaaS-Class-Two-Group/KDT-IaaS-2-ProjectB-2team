import React from "react";
import { useRouter } from "next/router";
import Image from "next/image";

const MainPage: React.FC = () => {
  const router = useRouter();

  return (
    <div className="h-screen flex flex-col items-center justify-center">
      {/* 이미지 영역 */}
      <div className="relative flex items-center justify-center w-full max-w-[1000px]">
        <Image
          src="/images/Title.png"
          alt="Title"
          width={573} // 원하는 기본 너비 (1000px로 확대)
          height={532} // 원하는 기본 높이
          priority
          className="object-contain" // 비율 유지 및 반응형 적용
        />
      </div>

      {/* 버튼 영역 */}
      <div className="w-4/5 flex justify-end mt-4 md:w-[35%]">
        <button
          onClick={()=>{router.push("/userpage")}}
          className="px-5 py-3 bg-[#332F47CC] rounded border border-[#D9C4B2]
                     font-cfont text-lg text-[#C5C1C3] hover:bg-[#D9C4B2CC] hover:text-black"
        >
          게임 시작
        </button>
      </div>
    </div>
  );
};

export default MainPage;