import React from 'react';

const MainPage: React.FC = () => {
  const handleStartClick = () => {
    window.location.href = '/UserPage';
  };

  return (
    <div id="root">
      <div>
        <h1>Zom 이상하다고 생각은 했지만<br/>Bi 상사태가 발생했습니다.</h1>
      </div>
      <div>
        <p>이미지분석시뮬레이션모델 머신러닝 투 좀비 이거 보여주려고 어그로 끌었다 좀비 실화냐?</p> 
      </div>
      <div>
        <button onClick={handleStartClick}>시작</button>
      </div>
    </div>
  );
};

export default MainPage;