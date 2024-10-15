import React, { useState ,useContext } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/router';
import '../app/globals.css';
import { UserContext } from '@/components/context';

const UserPage: React.FC = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("UserContext must be used within a UserProvider");
  }
  const { userData , setUserData } = context;

  const userouter = useRouter();
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState(''); 

  const handleInputChange = (basicdata: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(basicdata.target.value);
  };

  const handleSelectChange = (basicdata: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(basicdata.target.value);
  };

  const handleImageChange = (basicdata: React.ChangeEvent<HTMLInputElement>) => {
    if (basicdata.target.files) {
      const selectedImage = basicdata.target.files[0];
      setImage(selectedImage);
      
      // FileReader를 사용하여 이미지 미리보기 생성
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string); 
      };
      reader.readAsDataURL(selectedImage); 
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!inputValue || !selectedOption || selectedOption === '선택' || !image) {
      setErrorMessage('모두 입력하세요.');
      return; 
    }

    const formData = new FormData();
    formData.append("nickname",inputValue);
    formData.append("region", selectedOption)
    if (image) formData.append('image', image);

    try {
      const response = await fetch('http://127.0.0.1:8000/result', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json()
      console.log(result)
      console.log(result.message)
      // console.log(URL.createObjectURL(image))

      if (response.ok) {
        setUserData({
          result : result.message
        });
        console.log(userData);
        userouter.push('/PreDict')
      } else {
        console.error('서버 오류:', response.statusText);
      }
      
    } catch (error) {
      console.error('요청 오류:', error);
    }
  };

  return (
    <div id="root" className="flex flex-col items-center space-y-4 p-4 bg-gray-200">
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4 w-4/5">
      <div className="w-full p-2 mb-4 bg-gray-400 text-white rounded">
        이름 : 
        <input 
          type="name" 
          name="name"
          value={inputValue} 
          onChange={handleInputChange} 
          placeholder="이름을 입력하세요" 
          className='bg-gray-400 text-white placeholder-white'
        />
      </div>
      <div className="w-full p-2 mb-4 bg-gray-400 rounded">
        <label htmlFor="region" className='text-white'>지역 : </label>
        <select id="region" value={selectedOption} onChange={handleSelectChange} className='bg-gray-400 text-white'>
          <option value="선택" className='text-white'>선택하세요</option>
          <option value="대전">대전</option>
          <option value="대구">대구</option>
          <option value="부산">부산</option>
          <option value="광주">광주</option>
          <option value="제주도">제주도</option>
        </select>
      </div>
      
      <label htmlFor="img" className={`w-full h-1000 bg-gray-400 text-white flex items-center justify-center rounded mb-4 ${imagePreview ? 'hidden' : ''}`}>
        이미지를 업로드하세요.
        <input id="img" type="file" onChange={handleImageChange} className="hidden" />
      </label>
      {imagePreview && (
        <div className="mt-4 relative w-full h-screen max-w-[700px]">
          <Image 
          src={imagePreview} 
          alt="Preview" 
          className="w-full h-64 object-cover mb-4 border rounded" 
          layout="fill" // 레이아웃 안에 꽉 찬 이미지
          objectFit="contain" // objectFit 속성 수정: objectFit을 contain으로 설정
        />
        </div>
      )}

      {errorMessage && <p className="text-red-500">{errorMessage}</p>} 
      <button type="submit" className='flex bg-gray-400 text-white w-1/6 justify-center items-end'>시작</button>
      </form>
    </div>
  );
};

export default UserPage;
