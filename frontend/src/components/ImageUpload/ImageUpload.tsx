import React, { useRef } from "react";
import { ImageUploadPreviewProps } from "./ImageUpload.interface";

const ImageUploadPreview: React.FC<ImageUploadPreviewProps> = ({ onImageChange, imagePreview }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedImage = event.target.files[0];
      onImageChange(selectedImage); // 부모의 콜백 호출, 파일 전달
    }
  };

  return (
    <div className="w-full flex flex-col items-center">
      <div
        onClick={() => fileInputRef.current?.click()}
        className={`relative w-full max-w-[20rem] h-[20rem] bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] flex items-center justify-center cursor-pointer ${
          imagePreview ? "p-0" : "p-4"
        }`}
      >
        {imagePreview ? (
          <img
            src={imagePreview}
            alt="Preview"
            className="w-full h-full object-contain rounded"
          />
        ) : (
          <span>이미지를 업로드하세요</span>
        )}
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="hidden"
      />
    </div>
  );
};

export default ImageUploadPreview;