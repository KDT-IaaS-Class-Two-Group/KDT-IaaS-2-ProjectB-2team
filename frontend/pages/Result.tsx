import React from 'react';
import { useLocation } from 'react-router-dom';

interface ResultState {
  nickname: string;
  region: string;
  image: File | null;
  prediction: string;
}

const Result: React.FC = () => {
  const location = useLocation();
  const { nickname, region, image, prediction } = location.state as ResultState;

  return (
    <div /*style={{ textAlign: 'center' }}*/>
      <h1>Result Page</h1>
      <p><strong>Nickname:</strong> {nickname}</p>
      <p><strong>Region:</strong> {region}</p>
      <p><strong>Prediction:</strong> {prediction}</p>
      {image && <img src={URL.createObjectURL(image)} alt="Uploaded" /*style={{ width: '200px', height: '200px' }} *//>}
    </div>
  );
}

export default Result;