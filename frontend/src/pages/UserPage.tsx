import React, { useState } from "react";
import Image from "next/image";
import "../app/globals.css";

const UserPage: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
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
    if (!inputValue || !selectedOption || selectedOption === "선택" || !image) {
      setErrorMessage("모두 입력하세요.");
      return;
    }

    const formData = new FormData();
    formData.append("nickname", inputValue); // 필드명을 'nickname'으로 설정
    formData.append("region", selectedOption); // 필드명을 'region'으로 설정
    if (image) formData.append("img", image); // 'img' 필드로 이미지 추가

    try {
      const response = await fetch("http://127.0.0.1:8000/result", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        window.location.href = `/PreDict?nickname=${inputValue}&region=${selectedOption}`;
        response;
      } else {
        console.error("서버 오류:", response.statusText);
      }
    } catch (error) {
      console.error("요청 오류:", error);
    }
  };

  return (
    <div
      id="root"
      className="flex flex-col items-center space-y-4 p-4 bg-gray-200"
    >
      <div className="w-full p-2 mb-4 bg-gray-600 text-white rounded">
        이름 :
        <input
          type="name"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="이름을 입력하세요"
          className="bg-gray-600 text-white placeholder-white"
        />
      </div>
      <div className="w-full p-2 mb-4 bg-gray-600 rounded">
        <label htmlFor="region" className="text-white">
          지역 :{" "}
        </label>
        <select
          id="region"
          value={selectedOption}
          onChange={handleSelectChange}
          className="bg-gray-600 text-white"
        >
          <option value="선택" className="text-white">
            선택하세요
          </option>
          <option value="대전">대전</option>
          <option value="대구">대구</option>
          <option value="부산">부산</option>
          <option value="광주">광주</option>
          <option value="제주도">제주도</option>
        </select>
      </div>
      <label
        htmlFor="img"
        className={`w-full h-64 bg-gray-600 text-white flex items-center justify-center rounded mb-4 ${
          imagePreview ? "hidden" : ""
        }`}
      >
        이미지를 업로드하세요.
        <input
          id="img"
          type="file"
          onChange={handleImageChange}
          className="hidden"
        />
      </label>
      {imagePreview && (
        <Image
          src={imagePreview}
          alt="Preview"
          className="w-full h-64 object-cover mb-4 border rounded"
          width={256} // 원하는 너비로 설정
          height={256} // 원하는 높이로 설정
        />
      )}
      {errorMessage && <p className="text-red-500">{errorMessage}</p>}
      <button
        onClick={handleSubmit}
        className="flex justify-end bg-gray-600 text-white rounded"
      >
        시작
      </button>
    </div>
  );
};

export default UserPage;
