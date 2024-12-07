// StatCard.tsx
import React from "react";
import { IStatCard } from "./StatCard.interface";



const StatCard: React.FC<IStatCard> = ({ userData, stat }) => {
  return (
    <div className="flex flex-col items-center">
      <div className="flex mb-2 space-x-1">
        {/* 닉네임 */}
        <div className="flex w-[97px] h-[22px] border-[#D9C4B2] border-2 items-center">
          <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">
            닉네임 :
          </div>
          <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">
            {userData.nickname}
          </div>
        </div>
        {/* 지역 */}
        <div className="flex w-[97px] h-[22px] border-[#D9C4B2] border-2 ">
          <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">
            지역:
          </div>
          <div className="flex w-1/2 bg-[#332F47CC] justify-center items-center text-[#C5C1C3] text-[8px] text-center">
            {userData.region}
          </div>
        </div>
      </div>
      {/* 능력치 */}
      <div className="flex border-[#D9C4B2] w-[198px] h-[72px] border-2">
        <div className="p-2 w-1/4 flex justify-center items-center text-[9px] text-center text-[#C5C1C3]">
          능력치
        </div>
        <div className="grid grid-cols-3 gap-1 w-3/4 p-1">
          {Object.entries(stat).map(([key, value]) => (
            <div
              key={key}
              className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]"
            >
              {key} : {value}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StatCard;