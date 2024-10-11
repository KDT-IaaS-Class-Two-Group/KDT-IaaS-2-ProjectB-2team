import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const goToPage = () => {
    navigate('/user');
  };
  return (
    <div /*style={{ textAlign: 'center' }}*/>
      <h1>Zom 이상하다고 생각은 했지만
           Bi 상사태가 발생했습니다.</h1>
      <h2>이미지분석시뮬레이션모델 머신러닝 투 좀비 이거 보여주려고 어그로 끌었다 좀비 실화냐?</h2>
      <button onClick={goToPage}>Go to User Input</button>
    </div>
  );
}

export default Home;