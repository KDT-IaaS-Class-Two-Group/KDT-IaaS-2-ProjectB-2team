import React from 'react';
import '../app/globals.css';

const MainPage: React.FC = () => {
  const handleStartClick = () => {
    window.location.href = '/UserPage';
  };

  return (
    <div id="root" className="flex flex-col items-center justify-center h-screen bg-gray-500">
      <div className="text-center">
        <h1 className="text-xl font-bold mb-4">
          Zom 이상하다고 생각은 했지만<br/>Bi 상사태가 발생했습니다.
        </h1>
      </div>
      <div className="mb-8">
        <p className="text-center">
          이미지분석시뮬레이션모델 머신러닝 투 좀비 이거 보여주려고 어그로 끌었다 좀비 실화냐?
        </p> 
      </div>
      <div>
        <button 
          onClick={handleStartClick} 
          className="px-4 py-2 bg-gray-300 text-black rounded"
        >
          게임 시작
        </button>
      </div>
    </div>
  );
};

export default MainPage;