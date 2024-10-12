import React, { useEffect, useState } from 'react';
import '../app/globals.css';

interface Response {
  img : string
  species: number;
  attack: string;
  defense: string;
  accuracy: string;
  weight: string;
}


const Predict: React.FC  = () => {
    const [data, setData] = useState<Response | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [nickname, setNickname] = useState<string>('');
    const [region, setRegion] = useState<string>('');
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/result', {
            method: 'POST',
          });
  
          if (!response.ok) {
            throw new Error('서버 응답 오류');
          }
  
          const result = await response.json();
          setData(result.message);
        } catch (error: unknown) {
          if (error instanceof Error) {
            setError(error.message);
          } else {
            setError('알 수 없는 오류가 발생했습니다.');
          }
        } finally {
          setLoading(false);
        }
      };

      const urlParams = new URLSearchParams(window.location.search);
      setNickname(urlParams.get('nickname') || '');
      setRegion(urlParams.get('region') || '');
    
      fetchData();
    }, []);
  
    if (loading) {
      return <p>로딩 중...</p>;
    }
  
    if (error) {
      return <p>에러: {error}</p>;
    }
  
    if (!data) {
      return <p>데이터를 찾을 수 없습니다.</p>;
    }
    
    const handleSubmit = () => {
      window.location.href = '/';
    };
    return (
      <div id="root" className="bg-gray-200 p-4 flex flex-col">
        <div className="text-xl font-bold mb-4 flex justify-center">사망 보고서</div>
        <div className="flex mb-4 bg-gray-400 p-2">
          <div className="w-1/4 bg-gray-500 flex justify-center items-center text-white">
            이미지 : {data.img}
          </div>
          <div className="w-3/4 bg-gray-200 flex">
            <div className="w-3/4 p-2">
              <div className="flex justify-evenly mb-2">
                <div className="bg-gray-300 p-1">닉네임 : {nickname}</div>
                <div className="bg-gray-300 p-1">지역 : {region}</div>
              </div>
              <div className="flex">
                <div className="bg-gray-300 p-2 w-1/4">능력치</div>
                <div className="grid grid-cols-2 gap-1 w-3/4 bg-gray-100 p-2">
                  <div>체력 : 100</div>
                  <div>공격력: {data.attack}</div>
                  <div>방어력: {data.defense}</div>
                  <div>정확도: {data.accuracy}</div>
                  <div>민첩성: 없는디 머여?</div>
                  <div>무게: {data.weight}</div>
                </div>
              </div>
            </div>
            <div className="w-1/4 flex justify-center items-center text-white bg-gray-600 text-xl text-6xl">10일
            </div>
          </div>
        </div>
    
        <div className="text-lg font-bold mb-2">사망 이력</div>
        <ul className="bg-white p-2 mb-4 border border-gray-400">
          {[...Array(6)].map((_, i) => (
            <li key={i} className="mb-1 border-b border-gray-300 py-2 px-2">
              Day {i + 1}: 내용
            </li>
          ))}
        </ul>
        <div>
        <button onClick={handleSubmit} className="bg-blue-500 text-white py-1 px-4 rounded mt-2">다시 시작</button>
        </div>
      </div>
    );
}
export default Predict