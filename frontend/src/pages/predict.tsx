import React from "react";
import { useUserContext } from "@/components/hooks/useUserContext";
import StatCard from "@/components/statCard/StatCard";
import DeathLog from "@/components/DeathLog/DeathLog";
import Link from "next/link";

const Predict: React.FC = () => {
  const { userData } = useUserContext();
  console.log(userData);

  return (
    <div className="p-4 flex flex-col items-center justify-center relative">
      <div className="absolute top-0 inset-0 flex flex-col items-center justify-center">
        <div className="flex bg-[#332F47CC] p-2 rounded border border-[#D9C4B2] w-[464px] h-[120px]">
          <div className="flex justify-center items-center mr-2">
            <div className="relative w-[85px] h-[102px] overflow-hidden">
              {userData?.img && (
                <div className="flex justify-center items-center bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 text-[40px]">
                  <img
                    src={`data:image/png;base64,${userData.img}`}
                    alt="Uploaded"
                    className="object-cover w-full h-full"
                  />
                </div>
              )}
            </div>
          </div>

          <div className="w-5/6 bg-[#332F47CC] flex">
            {userData && userData.stat && (
              <StatCard
                userData={{
                  nickname: userData.nickname,
                  region: userData.region,
                }}
                stat={userData.stat}
              />
            )}
          </div>
        </div>

        <div className="mb-3" />
        <div className="w-[464px] bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 p-4 flex flex-col items-center">
          <h2 className="text-[17px] font-bold mb-4">사망 이력</h2>
          <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] p-3 mb-4">
            {userData?.log ? (
              <DeathLog deathLogProps={userData.log} />
            ) : (
              <p className="text-sm text-gray-500">사망 이력이 없습니다.</p>
            )}
          </div>
          <Link
            className="bg-blue-500 text-white py-2 px-4 rounded mt-2 hover:bg-blue-700"
            href={"/userpage"}
          >
            다시 시작
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Predict;