import React, { useState } from "react";
import { useRouter } from "next/router";
import { useUserContext } from "@/hooks/useUserContext"; // useUserContext 훅 가져오기
import RegionList from "@/components/RegionList";

const UserPage: React.FC = () => {
  const { setUserData } = useUserContext(); // useUserContext를 통해 context 값 가져오기
  const router = useRouter();

  const [inputValue, setInputValue] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(event.target.value);
  };

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const selectedImage = event.target.files[0];
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
    formData.append("nickname", inputValue);
    formData.append("region", selectedOption);
    if (image) formData.append("img", image);

    try {
      const response = await fetch("http://127.0.0.1:8000/result", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      console.log(result);

      if (response.ok) {
        setUserData(result); // 서버 응답을 userData에 저장
        router.push("/predict");
      } else {
        console.error("서버 오류:", response.statusText);
      }
    } catch (error) {
      console.error("요청 오류:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen p-4">
      <div></div>
      <div></div>
      <div className="relative flex flex-col items-center w-full max-w-xl">
        <div className="w-[500px] mb-4 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] flex">
          닉네임 :
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="닉네임을 입력하세요"
            className="bg-[#332F47CC] text-[#C5C1C3] text-lg placeholder-white ml-2 w-full"
          />
        </div>

        <RegionList selectedOption={selectedOption} onSelectChange={handleSelectChange} />

        <label
          htmlFor="img"
          className={`w-[500px] h-[500px] mx-auto bg-[#332F47CC] rounded border border-[#D9C4B2] 
          font-cfont text-[#C5C1C3] text-l flex items-center justify-center mb-4 ${
            imagePreview ? "hidden" : ""
          }`}
        >
          이미지를 업로드하세요.
          <input id="img" type="file" onChange={handleImageChange} className="hidden" />
        </label>

        {imagePreview && (
          <div className="mt-4 relative w-full h-[500px] max-w-[500px] max-h-[500px] mx-auto">
            <img src={imagePreview} alt="Preview" className="w-full h-full object-contain mb-4 border rounded" />
          </div>
        )}

        {errorMessage && <p className="text-red-500">{errorMessage}</p>}

        <button
          onClick={handleSubmit}
          className="mt-4 px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black"
        >
          시작
        </button>
      </div>
    </div>
  );
};

export default UserPage;