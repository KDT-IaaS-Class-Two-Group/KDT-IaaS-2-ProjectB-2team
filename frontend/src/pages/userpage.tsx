import React, { useRef, useState } from "react";
import { useRouter } from "next/router";
import { useUserContext } from "@/components/hooks/useUserContext";
import RegionList from "@/components/RegionList/RegionList";
import NicknameInput from "@/components/NicknameInput/NicknameInput";
import ImageUploadPreview from "@/components/ImageUpload/ImageUpload";

const UserPage: React.FC = () => {
  const { setUserData } = useUserContext();
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const selectRef = useRef<HTMLSelectElement>(null);

  // 이미지 파일과 미리보기 URL을 부모에서 관리
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  // 자식에서 호출될 콜백 함수: 이미지 파일과 미리보기 URL을 설정
  const handleImageChange = (file: File) => {
    setImageFile(file);

    // 미리보기 URL 생성
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async () => {
    const inputValue = inputRef.current?.value || "";
    const selectedOption = selectRef.current?.value || "";

    if (!inputValue || !selectedOption || selectedOption === "선택" || !imageFile) {
      setErrorMessage("모두 입력하세요.");
      return;
    }

    const formData = new FormData();
    formData.append("nickname", inputValue);
    formData.append("region", selectedOption);
    formData.append("img", imageFile); // 이미지 파일 전송

    try {
      const response = await fetch("http://127.0.0.1:8000/result", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (response.ok) {
        setUserData(result);
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
        <NicknameInput inputRef={inputRef} />
      </div>
      <div className="h-1/6">
        <RegionList selectRef={selectRef} />
      </div>
      <div className="h-3/6">
        <ImageUploadPreview onImageChange={handleImageChange} imagePreview={imagePreview} /> {/* 콜백과 미리보기 전달 */}
      </div>
      <div className="h-1/6">
        <button onClick={handleSubmit}>제출</button>
      </div>
    </div>
  );
};

export default UserPage;