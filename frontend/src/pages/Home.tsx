import React from 'react';

const MainPage: React.FC = () => {
  const handleStartClick = () => {
    window.location.href = '/UserPage';
  };

  return (
    <div id="root" className="h-screen grid place-items-center text-center">
      <div>
        <h1 className="text-3xl font-bold mb-4">Zom 이상하다고 생각은 했지만<br/>Bi 상사태가 발생했습니다.</h1>
      </div>
      <div>
        <p className="text-lg mb-6">이미지분석시뮬레이션모델 머신러닝 투 좀비 이거 보여주려고 어그로 끌었다 좀비 실화냐?</p> 
      </div>
      <div>
        <button onClick={handleStartClick} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">시작</button>
      </div>
    </div>
    
  );
};

export default MainPage;