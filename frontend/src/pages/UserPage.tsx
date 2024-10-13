import React, { useState } from 'react';
import './styles/index.css';
import Image from 'next/image'; // Next.js의 Image 컴포넌트 import

const UserPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null); // 미리보기 상태 추가


  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(e.target.value);
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFile = e.target.files[0];
      setImage(selectedFile); // 파일 상태 업데이트
      const imageUrl = URL.createObjectURL(selectedFile); // 이미지 URL 생성
      setImagePreview(imageUrl); // 미리보기 상태 업데이트
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
        // const result = await response.json();
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
    <div className="w-full h-screen bg-gray-200 grid place-items-center">
      <div className="bg-gray-300 p-8 rounded-md w-[400px] max-h-screen grid gap-6">
        <div className="grid gap-2">
          <div className="text-gray-700 text-lg">닉네임 : </div>
          <input type="text" value={inputValue} onChange={handleInputChange} placeholder="닉네임을 입력하세요" 
          className="w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500"/>
        </div>

        <div className="grid gap-2">
          <label htmlFor="region" className="text-gray-700 text-lg">지역을 선택하세요. : </label>
          <select id= "region" value={selectedOption} onChange={handleSelectChange}
          className="w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500">
            <option value="">선택하세요</option>
            <option value="서울">서울</option>
            <option value="부산">부산</option>
            <option value="대구">대구</option>
            <option value="인천">인천</option>
            <option value="광주">광주</option>
            <option value="대전">대전</option>
            <option value="울산">울산</option>
            <option value="세종">세종</option>
            <option value="경기">경기</option>
            <option value="강원">강원</option>
            <option value="충북">충북</option>
            <option value="충남">충남</option>
            <option value="전북">전북</option>
            <option value="전남">전남</option>
            <option value="경북">경북</option>
            <option value="경남">경남</option>
            <option value="제주">제주</option>
          </select>
        </div>
      
        <div className="grid gap-2">
          <label htmlFor="userimg" className="text-gray-700 text-lg">이미지 미리보기 :</label>
          <input  id= "userimg" type="file" onChange={handleImageChange} className="w-full px-3 py-2 border border-gray-400 rounded-md"/>
          {imagePreview && ( // 이미지 미리보기를 표시
            <div className="mt-4 relative w-full h-0 pb-[100%]">
              <Image
                src={imagePreview} // Image 컴포넌트의 src로 미리보기 URL 사용
                alt="미리보기"
                layout="fill" // fill을 사용해 부모 div의 크기를 채움
                objectFit="cover" // 이미지 비율 유지하면서 크기 조정
                className="rounded-md border border-gray-400"
              />
            </div>
          )}
        </div>

        <div className="grid place-items-center">
         <button onClick={handleSubmit} 
          className="w-[150px] h-[50px] bg-black text-white rounded-md text-lg">시작</button>
        </div>
      </div>
    </div>
  );
};

export default UserPage;
