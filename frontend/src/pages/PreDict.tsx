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
      
      <div id="root" className="p-4 flex flex-col items-center justify-center">
        <UserProvider>
        <img src="/images/predict.png" alt="description" className="w-1080 min-h-1075 object-cover"/>
        <div className="absolute top-0 inset-0 flex flex-col items-center justify-center ">
        
        <div className="flex bg-[#332F47CC] p-2 rounded border border-[#D9C4B2] w-[464px] h-[120px]">
        <div className=" flex justify-center items-center mr-2">
          <div className="relative w-[85px] h-[102px] overflow-hidden">
            <Image
            src={img}
            alt="Uploaded"
            layout="fill" // 부모 div의 크기를 채우도록 설정
            className="object-cover"
            />
            </div>
            </div>
            
            <div className="w-5/6 bg-[#332F47CC] flex">
              <div className="w-3/4 flex flex-col items-center">
                <div className="flex mb-2 space-x-1">
                  <div className="flex w-[97px] h-[22px] border-[#D9C4B2] border-2 items-center">
                    <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">닉네임</div>
                    <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">{nickName}</div>
                  </div>
                  <div className="flex w-[97px] h-[22px] border-[#D9C4B2] border-2 ">
                    <div className="flex w-1/2 justify-center items-center text-[#C5C1C3] text-[8px] text-center">지역</div>
                    <div className="flex w-1/2 bg-[#332F47CC] justify-center items-center text-[#C5C1C3] text-[8px] text-center">{region}</div>
                  </div>
                </div>
                <div className="flex border-[#D9C4B2] w-[198px] h-[72px] border-2">
                  <div className="p-2 w-1/4 flex justify-center items-center text-[9px] text-center text-[#C5C1C3]">능력치</div>
                  <div className="grid grid-cols-3 gap-1 w-3/4 p-1">
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">체력 : 100</div>
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">공격력 : {stat.attack}</div>
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">방어력 : {stat.defense}</div>
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">정확도 : {stat.accuracy}</div>
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">민첩성 : 10</div>
                    <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 flex justify-center items-center text-center text-[7px]">무게 : {stat.weight}</div>
                  </div>
                </div>
              </div>
              <div className=""> </div>
              <div className="w-1/4 flex justify-center items-center bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 text-[40px]">
                {log.length}일
              </div>
            </div>
          </div>

        <div className="mb-3" />
        <div className="w-[464px] bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2 p-4 flex flex-col items-center">

        <h2 className="text-[17px] font-bold mb-4">사망 이력</h2>
        <div className="bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] p-3 mb-4">
          
            <ul className="list-disc space-y-2">
              {[...Array(log.length)].map((_, i) => (
                <li key={i} className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2]">
                  {i + 1}일차 : {Object.values(log[i])}
                </li>
              ))}
              {/* <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 1 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 2 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 1 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 2 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 1 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 2 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 1 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 2 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 1 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li>
              <li className="py-2 px-4 bg-[#332F47CC] text-[#C5C1C3] border-[#D9C4B2] border-2">day 2 : 강력한 적에게 패배했습니다. HP가 만큼 감소했습니다.</li> */}


            </ul>
          </div>
        
        
        <button onClick={handleSubmit} className="bg-blue-500 text-white py-2 px-4 rounded mt-2 hover:bg-blue-700">다시 시작</button>
      </div>


       
        </div>
        
      </UserProvider>
      </div>

    );
}
export default Predict