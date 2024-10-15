import React, { useContext } from 'react';
import '../app/globals.css';
import Image from 'next/image';
import { UserContext , UserProvider} from '@/components/context';


const Predict: React.FC = () => {
  const context = useContext(UserContext); // UserContext에서 데이터 받아오기
  if (!context) {
    throw new Error('UserContext must be used within a UserProvider');
  }

  const { userData } = context;
  console.log(userData)
  
  // userData에서 필요한 데이터를 구조분해할당으로 추출
  const { nickname, region, image, stats } = userData || {
    nickname: '',
    region: '',
    image: '',
    stats: { attack: 0, defense: 0, accuracy: 0, weight: 0 }
  };
  
  const handleSubmit = () => {
    window.location.href = '/';
  };

    return (
      
      <UserProvider>
      <div id="root" className="bg-gray-200 p-4 flex flex-col">
        <div className="text-xl font-bold mb-4 flex justify-center">사망 보고서</div>
        <div className="flex mb-4 bg-gray-400 p-2 rounded">
          <div className="w-1/4 bg-gray-200 flex justify-center items-center mr-5">
          이미지 : <Image src={image} alt="Uploaded" className="w-full h-64 object-cover" layout="fill" // 레이아웃 안에 꽉 찬 이미지
      objectFit="contain" /> {/* 이미지 출력 */}
          </div>
          <div className="w-3/4 bg-gray-200 flex p-2">
            <div className="w-3/4 p-2 flex flex-col">
              <div className="flex mb-2 ">
                <div className="flex w-1/2 border-white border-2">
                  <div className="flex w-1/2  p-1 justify-center mt-1">닉네임 </div>
                  <div className="flex w-1/2 bg-gray-400 p-1 m-1 justify-center">{nickname}</div>
                </div>
                <div className="flex w-1/2 border-white border-2">
                  <div className="flex w-1/2  p-1 justify-center mt-1">지역 </div>
                  <div className="flex w-1/2 bg-gray-400 p-1 m-1 justify-center">{region}</div>
                </div>
              </div>
              <div className="flex border-white border-2">
                <div className="p-2 w-1/4 flex justify-center items-center text-2xl">능력치</div>
                <div className="grid grid-cols-3 gap-1 w-3/4 p-2">
                  <div className="bg-gray-400 justify-center flex">체력 : 100</div>
                  <div className="bg-gray-400 justify-center flex">공격력: {stats.attack}</div>
                  <div className="bg-gray-400 justify-center flex">방어력: {stats.defense}</div>
                  <div className="bg-gray-400 justify-center flex">정확도: {stats.accuracy}</div>
                  <div className="bg-gray-400 justify-center flex">민첩성: 10</div>
                  <div className="bg-gray-400 justify-center flex">무게: {stats.weight}</div>
                </div>
              </div>
            </div>
            <div className="w-1/4 flex justify-center items-center text-white bg-gray-400 text-6xl">10일
            </div>
          </div>
        </div>
    
        <div className="text-lg font-bold bg-gray-400 w-1/3 flex justify-center rounded-t">사망 이력</div>
        <div className="bg-gray-400">
          <div className="bg-white m-2 pt-1 pb-1">
            <ul className=" p-2 m-2">
              {[...Array(6)].map((_, i) => (
                <li key={i} className="py-2 px-2  bg-gray-400 m-2 p-2 text-white">
                  Day {i + 1}: 내용
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div>
        <button onClick={handleSubmit} className="bg-blue-500 text-white py-1 px-4 rounded mt-2">다시 시작</button>
        </div>
      </div>

      </UserProvider>
    );
}
export default Predict