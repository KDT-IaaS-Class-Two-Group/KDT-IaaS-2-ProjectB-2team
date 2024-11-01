import React from "react";
// import '../app/globals.css';
import { useRouter } from "next/router";
const MainPage: React.FC = () => {
  const router = useRouter();

  const handleStartClick = () => {
    router.push("/predict");
  };

  return (
    <div
      className="flex flex-col items-center justify-center h-screen mx-40"
    >

      <div className="indexImage w-4/5 h-4/5 min-h-64 min-w-64">

      </div>
      <div className="mb-4">
        <button
          onClick={handleStartClick}
          className=" 
      px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] 
      font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black"
        >
          게임 시작
        </button>
      </div>
    </div>
  );
};

export default MainPage;
