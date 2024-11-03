import React from "react";
import { useRouter } from "next/router";
import Image from "next/image";

const MainPage: React.FC = () => {
  const router = useRouter();

  const handleStartClick = () => {
    router.push("/userpage");
  };

  return (
    <>
      <div className="min-h-[400px] min-w-[400px] relative">
        <Image
          src="/images/Title.png"
          alt="Title"
          fill
          style={{ objectFit: "contain" }}
          priority
        />
        <button
          onClick={handleStartClick}
          className="absolute bottom-[20%] right-[38%]
             px-5 py-3 bg-[#332F47CC] rounded border border-[#D9C4B2]
             font-cfont text-lg text-[#C5C1C3] hover:bg-[#D9C4B2CC] hover:text-black"
          style={{
            bottom: "20%",
            right: "calc(38% - 50px)",
          }}
        >
          게임 시작
        </button>
      </div>
    </>
  );
};

export default MainPage;
