export interface ImageUploadPreviewProps {
  onImageChange: (file: File) => void; // 파일 변경 콜백
  imagePreview: string | null; // 부모에서 전달받는 미리보기 URL
}