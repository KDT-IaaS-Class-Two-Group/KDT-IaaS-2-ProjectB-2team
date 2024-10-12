import React, { useState } from 'react';

const UserPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [image, setImage] = useState<File | null>(null);

  const handleInputChange = (basicdata: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(basicdata.target.value);
  };

  const handleSelectChange = (basicdata: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(basicdata.target.value);
  };

  const handleImageChange = (basicdata: React.ChangeEvent<HTMLInputElement>) => {
    if (basicdata.target.files) {
      setImage(basicdata.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('input', inputValue);
    formData.append('select', selectedOption);
    if (image) formData.append('image', image);

    try {
      const response = await fetch('http://127.0.0.1:8000/result', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        // 닉네임과 지역을 URL 매개변수로 전달
        window.location.href = `/PreDict?nickname=${inputValue}&region=${selectedOption}`;
      } else {
        console.error('서버 오류:', response.statusText);
      }
    } catch (error) {
      console.error('요청 오류:', error);
    }
  };

  return (
    <div>
      <div>닉네임 : </div>
      <input type="name" value={inputValue} onChange={handleInputChange} placeholder="닉네임을 입력하세요" />
      <label htmlFor="region">지역을 선택하세요. : </label>
      <select id="region" value={selectedOption} onChange={handleSelectChange}>
        <option value="선택">선택하세요</option>
        <option value="대전">대전</option>
        <option value="대구">대구</option>
        <option value="부산">부산</option>
        <option value="광주">광주</option>
        <option value="제주도">제주도</option>
      </select>
      <label htmlFor="img">이미지를 업로드하세요 : </label>
      <input id="img" type="file" onChange={handleImageChange} />
      <button onClick={handleSubmit}>시작</button>
    </div>
  );
};

export default UserPage;
