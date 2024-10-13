import React from 'react';

const MainPage: React.FC = () => {
  const handleStartClick = () => {
    window.location.href = '/UserPage';
  };

  return (
    <div id="root" className="w-[812px] h-screen bg-[#D9D9D9] grid place-items-center mx-auto my-auto">
      <div className="text-[38px] grid place-items-center absolute top-[280px] left-1/2 transform -translate-x-1/2">
        <h1>Zom 이상하다고 생각은 했지만<br/></h1>
        <h1>Bi 상사태가 발생했습니다.</h1>
      </div>
      <div className="w-[743px] h-[23px] text-[18px] grid place-items-center absolute top-[510px] left-1/2 transform -translate-x-1/2">
        <p>이미지분석시뮬레이션모델 머신러닝 투 좀비 이거 보여주려고 어그로 끌었다 좀비 실화냐?</p> 
      </div>
      <div>
        <button onClick={handleStartClick} className="w-[150px] h-[50px] bg-[#1E1E1E] text-white grid place-items-center absolute top-[610px] left-1/2 transform -translate-x-1/2">시작</button>
      </div>
    </div>
    
  );
};

export default MainPage;