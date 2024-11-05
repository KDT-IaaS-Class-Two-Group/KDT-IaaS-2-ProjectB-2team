import React, { useState } from "react";
import { useRouter } from "next/router";
import { useUserContext } from "@/components/hooks/useUserContext"; // useUserContext 훅 가져오기
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
    <div className="max-w-5xl h-full">
      <div className="h-1/6">
        <div></div>
        <div></div>
      </div>
  
      <div className="h-1/6">
        <RegionList selectedOption={selectedOption} onSelectChange={handleSelectChange} />
      </div>
  
      <div className="h-3/6"></div>
  
      <div className="h-1/6">
        <button></button>
      </div>
    </div>
  );
};

export default UserPage;