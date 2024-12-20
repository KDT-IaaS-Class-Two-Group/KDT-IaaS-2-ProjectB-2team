import React from "react";
import StatCard from "../StatCard/StatCard";
import { UserProfileProps } from "./UserProfile.interface";

const UserProfile: React.FC<UserProfileProps> = ({ userData, stat }) => {
  // ! 타입 가드 부분
  if (!userData || !stat) {
    return (
      <div className="flex justify-center items-center w-full h-full">
        <p className="text-sm text-gray-500">
          유효한 데이터를 불러올 수 없습니다.
        </p>
      </div>
    );
  }

  // ! 랜더링 부분
  return (
    <div className="flex justify-center items-center w-full p-4 bg-[#332F47CC] border-[#D9C4B2] border rounded-md mb-4">
      {/* 이미지 섹션 */}
      <div className="w-2/5 h-20 mr-4 relative">
          {userData.img ? (
            <img
              src={`data:image/png;base64,${userData.img}`}
              alt={`${userData.nickname}의 프로필 이미지`}
              className="absolute inset-0 object-cover w-full h-full"
            />
          ) : (
            <div className="flex items-center justify-center w-full h-full bg-gray-300 border-[#D9C4B2] border-2 rounded">
              <p className="text-sm text-gray-500">이미지 없음</p>
            </div>
          )}
      </div>

      {/* StatCard 섹션 */}
      <StatCard userData={userData} stat={stat} />
    </div>
  );
};

export default UserProfile;