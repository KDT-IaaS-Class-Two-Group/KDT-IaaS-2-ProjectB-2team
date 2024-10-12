import React, { useState } from 'react';
import '../app/globals.css';

const UserPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState(''); 

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
    if (!inputValue || !selectedOption || selectedOption === '선택' || !image) {
      setErrorMessage('모두 입력하세요.');
      return; // 조건을 만족하지 않으면 넘어가지 않음
    }

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
        window.location.href = `/PreDict?nickname=${inputValue}&region=${selectedOption}`;
      } else {
        console.error('서버 오류:', response.statusText);
      }
    } catch (error) {
      console.error('요청 오류:', error);
    }
  };

  return (
    <div id="root"  className="flex flex-col items-center space-y-4 p-4 bg-gray-200">
      <div className="w-full p-2 mb-4 bg-gray-600 text-white rounded">이름 : 
      <input type="name" value={inputValue} onChange={handleInputChange} placeholder="이름을 입력하세요" className=' bg-gray-600 text-white placeholder-white'/>
      </div>
      <div className="w-full p-2 mb-4 bg-gray-600 rounded">
        <label htmlFor="region" className='text-white'>지역 : </label>
        <select id="region" value={selectedOption} onChange={handleSelectChange} className='bg-gray-600 text-white'>
          <option value="선택" className='text-white'>선택하세요</option>
          <option value="대전">대전</option>
          <option value="대구">대구</option>
          <option value="부산">부산</option>
          <option value="광주">광주</option>
          <option value="제주도">제주도</option>
        </select>
      </div>
      <label htmlFor="img" className="w-full h-64 bg-gray-600 text-white flex items-center justify-center mb-4">이미지를 업로드하세요.</label>
      <input id="img" type="file" onChange={handleImageChange} className="hidden"/>
      {errorMessage && <p className="text-red-500">{errorMessage}</p>} 
      <button onClick={handleSubmit} className='flex justify-end bg-gray-600 text-white'>시작</button>
    </div>
  );
};

export default UserPage;
