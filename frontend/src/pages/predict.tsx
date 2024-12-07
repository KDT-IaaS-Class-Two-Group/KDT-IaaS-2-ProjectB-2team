import React from "react";
import { useUserContext } from "@/hooks/useUserContext";
import UserProfile from "@/components/UserProfile/UserProfile";
import DeathLog from "@/components/DeathLog/DeathLog";
import Link from "next/link";

const Predict: React.FC = () => {
  const { userData } = useUserContext();

  if (!userData) {
    return (
      <div className="flex justify-center items-center w-full h-screen">
        <p className="text-sm text-gray-500">
          유효한 사용자 데이터를 불러올 수 없습니다.
        </p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-96 h-full justify-center flex flex-col">
      <UserProfile
        userData={{
          nickname: userData.nickname,
          region: userData.region,
          img: userData.img,
        }}
        stat={userData.stat}
      />
      <DeathLog deathLogProps={userData.log} />
      <div className="w-full flex justify-center">
        <Link
          className="mt-4 px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black"
          href={"/userpage"}
        >
          다시 시작
        </Link>
      </div>
    </div>
  );
};

export default Predict;
