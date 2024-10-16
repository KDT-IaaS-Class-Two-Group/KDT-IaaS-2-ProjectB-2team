import React from 'react';
// import '../app/globals.css';
import { useRouter } from 'next/router';

const MainPage: React.FC = () => {
const router = useRouter()

  const handleStartClick = () => {
      router.push("/UserPage")
  };

  return (
    <div id="root" className="flex flex-col items-center justify-center h-screen ">
      <div className="relative mb-4">
      <img src="/images/index.png" alt="description" className="w-1080 h-screen object-cover" />
      <button onClick={handleStartClick}
      className="absolute top-[787px] left-[611px] 
      px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] 
      font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black">
        게임 시작
      </button>
      </div>
    </div>
  );
};

export default MainPage;