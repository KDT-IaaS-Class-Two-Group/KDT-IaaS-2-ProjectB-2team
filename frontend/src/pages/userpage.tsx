import React, { useRef, useState } from "react";
import { useRouter } from "next/router";
import { useUserContext } from "@/hooks/useUserContext";
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
  const [errorMessage, setErrorMessage] = useState(false); // errorMessage를 boolean으로 변경

  // 자식에서 호출될 콜백 함수: 이미지 파일과 미리보기 URL을 설정
  const handleImageChange = (file: File) => {
    setImageFile(file);
    setErrorMessage(false)

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

    // 모든 필드가 입력되지 않은 경우 에러 메시지 표시
    if (!inputValue || !selectedOption || selectedOption === "선택" || !imageFile) {
      setErrorMessage(true);
      return;
    }

    setErrorMessage(false); // 입력이 완료된 경우 에러 메시지 숨김

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
        // console.log(result) // ! 콘솔 찍어서 볼 수 있게. 배포 시 삭제 할 것
        router.push("/predict");
      } else {
        console.error("서버 오류:", response.statusText);
      }
    } catch (error) {
      console.error("요청 오류:", error);
    }
  };

  const changeHandler = ()=>{setErrorMessage(false)}


  return (
    <div className="w-full max-w-96 h-full pt-4 sm:pt-32 justify-around flex flex-col">
      <div className="mb-4">
        <NicknameInput inputRef={inputRef} changehandler={changeHandler}/>
      </div>
      <div className="mb-4">
        <RegionList selectRef={selectRef} changeHandler={changeHandler}/>
      </div>
      <div className="mb-4">
        <ImageUploadPreview onImageChange={handleImageChange} imagePreview={imagePreview} />
      </div>
      <div className="flex justify-center items-center flex-col">
        <span className={`text-red-500 min-h-8 ${errorMessage ? "inline" : "hidden"}`}>
          모두 입력하세요!
        </span>
        <button
          className="mt-4 px-4 py-2 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] text-lg hover:bg-[#D9C4B2CC] hover:text-black"
          onClick={handleSubmit}
        >
          시작!
        </button>
      </div>
    </div>
  );
};

export default UserPage;