import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';

const UserInput: React.FC = () => {
  const [nickname, setNickname] = useState<string>('');
  const [region, setRegion] = useState<string>('');
  const [image, setImage] = useState<File | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append('nickname', nickname);
    formData.append('region', region);
    if (image) {
      formData.append('image', image);
    }

    fetch('/predict', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        navigate('/result', { state: { nickname, region, image, prediction: data } });
      });
  };

  return (
    <div /*style={{ textAlign: 'center' }}*/>
      <h1>User Information</h1>
      <input
        type="text"
        placeholder="Enter Nickname"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
      />
      <br />
      <label htmlFor="region">Select your region:</label>
      <select id="region" value={region} onChange={(e) => setRegion(e.target.value)}>
        <option value="">Select Region</option>
        <option value="Daejeon">Daejeon</option>
        <option value="Seoul">Seoul</option>
        <option value="Busan">Busan</option>
      </select>
      <br />
      <input
        type="file"
        onChange={handleFileChange}
      />
      <br />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default UserInput;
