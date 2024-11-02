import React from "react";
import { useRouter } from "next/router";
import Image from "next/image";

const MainPage: React.FC = () => {
  const router = useRouter();

  const handleStartClick = () => {
    router.push("/userpage");
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen mx-4 sm:mx-8 lg:mx-40">
      <div className="relative w-full max-w-lg h-64 sm:h-72 md:h-96 lg:h-[500px] xl:h-[600px] min-h-[300px]">
        <Image
          src="/images/Title.png"
          alt="Title"
          fill
          sizes="(max-width: 640px) 100vw, (max-width: 768px) 75vw, (max-width: 1024px) 50vw, 33vw"
          style={{ objectFit: "contain" }}
        />
        <button
          onClick={handleStartClick}
          className="absolute bottom-4 sm:bottom-6 md:bottom-8 lg:bottom-10 left-1/2 transform -translate-x-1/2 
                     px-3 sm:px-4 md:px-5 py-1 sm:py-2 md:py-3 bg-[#332F47CC] rounded border border-[#D9C4B2]
                     font-cfont text-sm sm:text-base md:text-lg lg:text-xl text-[#C5C1C3] hover:bg-[#D9C4B2CC] hover:text-black"
        >
          게임 시작
        </button>
      </div>
    </div>
  );
};

export default MainPage;