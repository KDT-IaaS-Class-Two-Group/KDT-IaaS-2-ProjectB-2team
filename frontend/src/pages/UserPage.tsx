import React, { useState ,useContext } from 'react';
import { useRouter } from 'next/router';
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
  const [errorMessage, setErrorMessage] = useState("");

  const handleInputChange = (
    basicdata: React.ChangeEvent<HTMLInputElement>
  ) => {
    setInputValue(basicdata.target.value);
  };

  const handleSelectChange = (
    basicdata: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setSelectedOption(basicdata.target.value);
  };

  const handleImageChange = (
    basicdata: React.ChangeEvent<HTMLInputElement>
  ) => {
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

  const handleSubmit = async () => {

    if (!inputValue || !selectedOption || selectedOption === '선택' || !image) {
      setErrorMessage('모두 입력하세요.');
      return; 
    }

    const formData = new FormData();
    formData.append("nickname",inputValue);
    formData.append("region", selectedOption)
    if (image) formData.append('img', image);

    try {
      const response = await fetch("http://127.0.0.1:8000/result", {
        method: "POST",
        body: formData,
      });
      const result = await response.json()
      console.log(result)
      console.log(result.message)

      if (response.ok) {
        setUserData(result);
        console.log(userData);
        userouter.push('/PreDict')
      } else {
        console.error("서버 오류:", response.statusText);
      }
      
    } catch (error) {
      console.error("요청 오류:", error);
    }
  };

  return (
    <div id="root" className="flex flex-col items-center justify-center h-screen">
      <div className="relative mb-4">
        <img src="/images/userpage.png" alt="description" className="w-[1080px] h-[1075px] object-cover" />

        <div className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center p-4">
          <div className="w-[500px] p-2 mb-4 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] text-lg flex items-center">
            닉네임 : 
            <input 
              type="name" 
              value={inputValue} 
              onChange={handleInputChange} 
              placeholder="닉네임을 입력하세요" 
              className='bg-[#332F47CC] text-[#C5C1C3] text-lg placeholder-white'
            />
          </div>
          
          <div className="w-[500px] p-2 mb-4 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont">
            <label htmlFor="region" className='text-[#C5C1C3] font-cfont'>지역 : </label>
            <select id="region" value={selectedOption} onChange={handleSelectChange} className='bg-[#332F47CC] text-[#C5C1C3]'>
              <option value="선택" className='font-cfont text-[#C5C1C3] text-lg'>선택하세요</option>
              <option value="대전" className='font-cfont text-[#C5C1C3] text-lg'>대전</option>
              <option value="대구" className='font-cfont text-[#C5C1C3] text-lg'>대구</option>
              <option value="부산" className='font-cfont text-[#C5C1C3] text-lg'>부산</option>
              <option value="광주" className='font-cfont text-[#C5C1C3] text-lg'>광주</option>
              <option value="제주도" className='font-cfont text-[#C5C1C3] text-lg'>제주도</option>
            </select>
          </div>

          <label htmlFor="img" className={`w-[500px] h-[500px] mx-auto bg-[#332F47CC] rounded border border-[#D9C4B2] 
            font-cfont text-[#C5C1C3] text-l flex items-center justify-center mb-4 ${imagePreview ? 'hidden' : ''}`}>
            이미지를 업로드하세요.
            <input id="img" type="file" onChange={handleImageChange} className="hidden" />
          </label>

          {imagePreview && (
            <div className="mt-4 relative w-full h-[500px] max-w-[500px] max-h-[500px] mx-auto">
              <img 
                src={imagePreview} 
                alt="Preview" 
                className="w-full h-full object-contain mb-4 border rounded" 
              />
            </div>
          )}


          {errorMessage && <p className="text-red-500">{errorMessage}</p>}
          
          <button onClick={handleSubmit} className='mt-4 px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black'>
            시작
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserPage;
