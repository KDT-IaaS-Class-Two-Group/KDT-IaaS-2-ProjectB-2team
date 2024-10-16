import React, { useContext } from 'react';
import '../app/globals.css';
import Image from 'next/image';
import { UserContext , UserProvider} from '@/components/context';


const Predict: React.FC = () => {
  const data = useContext(UserContext); // UserContext에서 데이터 받아오기
  if (!data) {
    throw new Error('UserContext must be used within a UserProvider');
  }

  const { userData } = data;
  console.log(userData)
  // userData?.result
  
  const {nickName , region , img, stat, log} = userData?.result || {
    nickName: "",
    region: "",
    img: "",
    stat: {
      species : 0,
      attack: 0,
      defense: 0,
      accuracy: "",
      weight: 0
    },
    log: []
  };
  
  const handleSubmit = () => {
    window.location.href = '/';
  };

    return (
      
      <div id="root" className="bg-gray-200 p-4 flex flex-col">
        <UserProvider>
        <div className="text-xl font-bold mb-4 flex justify-center">사망 보고서</div>
        <div className="flex mb-4 bg-gray-400 p-2 rounded">
          <div className="w-1/4 bg-gray-200 flex justify-center items-center mr-5 ">
          <Image src={img} alt="Uploaded" width={200} height={200} className=" object-cover w-auto h-auto "
      objectFit="contain" /> 
          </div>
          <div className="w-3/4 bg-gray-200 flex p-2">
            <div className="w-3/4 p-2 flex flex-col">
              <div className="flex mb-2 ">
                <div className="flex w-1/2 border-white border-2">
                  <div className="flex w-1/2  p-1 justify-center mt-1">닉네임 </div>
                  <div className="flex w-1/2 bg-gray-400 p-1 m-1 justify-center">{nickName}</div>
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
                  <div className="bg-gray-400 justify-center flex">공격력: {stat.attack}</div>
                  <div className="bg-gray-400 justify-center flex">방어력: {stat.defense}</div>
                  <div className="bg-gray-400 justify-center flex">정확도: {stat.accuracy}</div>
                  <div className="bg-gray-400 justify-center flex">민첩성: 10</div>
                  <div className="bg-gray-400 justify-center flex">무게: {stat.weight}</div>
                </div>
              </div>
            </div>
            <div className="w-1/4 flex justify-center items-center text-white bg-gray-400 text-6xl"> {log.length}일
            </div>
          </div>
        </div>
    
        <div className="text-lg font-bold bg-gray-400 w-1/3 flex justify-center rounded-t">사망 이력</div>
        <div className="bg-gray-400">
          <div className="bg-white m-2 pt-1 pb-1">
            <ul className=" p-2 m-2">
              {[...Array(log.length)].map((_, i) => (
                <li key={i} className="py-2 px-2  bg-gray-400 m-2 p-2 text-white">
                  {i + 1}일차 :  {Object.values(log[i])} 
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div>
        <button onClick={handleSubmit} className="bg-blue-500 text-white py-1 px-4 rounded mt-2">다시 시작</button>
        </div>
      </UserProvider>
      </div>

    );
}
export default Predict