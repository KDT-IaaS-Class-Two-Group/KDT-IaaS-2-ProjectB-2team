import { useState } from "react";

interface Response {
  species: number;
  attack: string;
  defense: string;
  accuracy: string;
  weight: string;
}

const Hello = () => {
  const [message, setMessage] = useState<Response | null>(null); //데이터 받기
  const [loading, setLoading] = useState<boolean>(false); //로딩
  const [error, setError] = useState<string | null>(null); //에러
  const [image, setImage] = useState<File | null>(null); //이미지 처리 

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      setImage(file);
      setError(null); // 오류 초기화
    }
  };

  const handleSubmit = async () => {
    if (!image) {
      setError("이미지를 먼저 선택해주세요.");
      return;
    }

    setLoading(true);
    setError(null); // 이전 오류 초기화
    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await fetch(`http://127.0.0.1:8000/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('응답이 올바르지 않음');
      }

      const responseData = await response.json();
      setMessage(responseData);
      
    } catch (error : unknown) {
      if (error instanceof Error) {
        setError("이미지 전송 중 오류 발생: " + error.message);
      } else {
        setError("알 수 없는 오류 발생");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="root">
      <div >
        <h2>이미지 업로드</h2>
        <input type="file" placeholder="이미지 업로드" accept="image/*" onChange={handleImageChange} />
      </div>

      <div >
        {loading && <p>로딩 중...</p>}
        {error && <p>{error}</p>}
        {message && (
          <>
            <h1>인종: {message.species}</h1>
            <h1>공격력: {message.attack}</h1>
            <h1>방어력: {message.defense}</h1>
            <h1>명중률: {message.accuracy}</h1>
            <h1>무게: {message.weight}</h1>
          </>
        )}
        <div>
          <button type="button" onClick={handleSubmit}>이미지 전송</button>
        </div>
      </div>
    </div>
  );
};

export default Hello;
