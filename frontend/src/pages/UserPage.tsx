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

    window.location.href = '/predict'; // 페이지 이동
  };

  return (
    <div>
      <input type="text" value={inputValue} onChange={handleInputChange} placeholder="입력하세요" />
      <label htmlFor="ddd">123</label>
      <select id= "ddd" value={selectedOption} onChange={handleSelectChange}>
        <option value="">선택하세요</option>
        <option value="option1">옵션 1</option>
        <option value="option2">옵션 2</option>
      </select>
      <label htmlFor="aaa">asd</label>
      <input  id= "aaa" type="file" onChange={handleImageChange} />
      <button onClick={handleSubmit}>예측하기</button>
    </div>
  );
};

export default UserPage;
