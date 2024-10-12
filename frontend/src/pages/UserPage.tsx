import React, { useState } from 'react';

const UserPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [image, setImage] = useState<File | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(e.target.value);
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('input', inputValue);
    formData.append('select', selectedOption);
    if (image) formData.append('image', image);

    await fetch('/result', {
      method: 'POST',
      body: formData,
    });

    window.location.href = '/PreDict'; // 페이지 이동
  };

  return (
    <div>
      <div>닉네임 : </div>
      <input type="text" value={inputValue} onChange={handleInputChange} placeholder="닉네임을 입력하세요" />
      <label htmlFor="region">지역을 선택하세요. : </label>
      <select id= "region" value={selectedOption} onChange={handleSelectChange}>
        <option value="">선택하세요</option>
        <option value="option1">대전</option>
        <option value="option2">대구</option>
        <option value="option3">부산</option>
        <option value="option4">광주</option>
        <option value="option5">제주도</option>
      </select>
      <label htmlFor="userimg">.</label>
      <input  id= "userimg" type="file" onChange={handleImageChange} />
      <button onClick={handleSubmit}>시작</button>
    </div>
  );
};

export default UserPage;
