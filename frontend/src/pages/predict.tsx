import React from "react";
import { useUserContext } from "@/hooks/useUserContext";
import UserProfile from "@/components/UserProfile/UserProfile";
import DeathLog from "@/components/DeathLog/DeathLog";



const Predict: React.FC = () => {
  const { userData } = useUserContext();

  if (!userData) {
    return (
      <div className="flex justify-center items-center w-full h-screen">
        <p className="text-sm text-gray-500">유효한 사용자 데이터를 불러올 수 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col w-full h-full">
      <UserProfile
        userData={{
          nickname: userData.nickname,
          region: userData.region,
          img: userData.img,
        }}
        stat={userData.stat}
      />
      <DeathLog deathLogProps={userData.log} />
    </div>
  );
};

export default Predict;