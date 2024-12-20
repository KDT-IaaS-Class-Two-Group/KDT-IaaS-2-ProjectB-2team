import React from "react";
import convertKey from "@/modules/convertKey";
import { IStatCard } from "./StatCard.interface";
import statTable from "@/shared/StatTable";

const StatCard: React.FC<IStatCard> = ({ userData, stat }) => {
  return (
    <div className="flex flex-col items-center w-full">
      {/* 닉네임 및 지역 */}
      <div className="flex w-full mb-2 space-x-2">
        <div className="flex flex-1 h-6 border border-gray-300 items-center rounded">
          <span className="flex-1 text-xs text-center text-[#b5bcc8]">
            닉네임:
          </span>
          <span className="flex-1 text-xs text-center text-[#C5C1C3]">
            {userData.nickname}
          </span>
        </div>
        <div className="flex flex-1 h-6 border border-gray-300 items-center rounded">
          <span className="flex-1 text-xs text-center text-[#b5bcc8]">
            지역:
          </span>
          <span className="flex-1 text-xs text-center text-[#C5C1C3]">
            {userData.region}
          </span>
        </div>
      </div>
      {/* 능력치 */}
      <div className="flex flex-col w-full border border-gray-300 rounded p-2">
        <div className="text-xs text-[#b5bcc8] mb-2 text-center">능력치</div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {Object.entries(stat).map(([key, value], index) => (
            <div
              key={index}
              className="bg-gray-200 text-gray-700 text-center text-xs border border-gray-300 rounded p-1"
            >
              {convertKey(key, statTable)}: {value}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StatCard;
