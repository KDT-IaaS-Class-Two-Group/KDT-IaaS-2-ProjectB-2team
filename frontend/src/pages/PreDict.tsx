import React, { useEffect, useState } from "react";
import "../app/globals.css";

interface Response {
  img: string;
  species: number;
  attack: string;
  defense: string;
  accuracy: string;
  weight: string;
}

const Predict: React.FC = () => {
  const [data, setData] = useState<Response | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [nickname, setNickname] = useState<string>("");
  const [region, setRegion] = useState<string>("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
        });

        if (!response.ok) {
          throw new Error("서버 응답 오류");
        }

        const result = await response.json();
        setData(result.message);
      } catch (error: unknown) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("알 수 없는 오류가 발생했습니다.");
        }
      } finally {
        setLoading(false);
      }
    };

    const urlParams = new URLSearchParams(window.location.search);
    setNickname(urlParams.get("nickname") || "");
    setRegion(urlParams.get("region") || "");

    fetchData();
  }, []);

  if (loading) {
    return <p>로딩 중...</p>;
  }

  if (error) {
    return <p>에러: {error}</p>;
  }

  if (!data) {
    return <p>데이터를 찾을 수 없습니다.</p>;
  }

  const handleSubmit = () => {
    window.location.href = "/";
  };
  return (
    <div id="root" className="bg-gray-200 p-4 flex flex-col">
      <div className="text-xl font-bold mb-4 flex justify-center">
        사망 보고서
      </div>
      <div className="flex mb-4 bg-gray-400 p-2 rounded">
        <div className="w-1/4 bg-gray-200 flex justify-center items-center mr-5">
          이미지 : {data.img}
        </div>
        <div className="w-3/4 bg-gray-200 flex p-2">
          <div className="w-3/4 p-2 flex flex-col">
            <div className="flex mb-2 ">
              <div className="flex w-1/2 border-white border-2">
                <div className="flex w-1/2  p-1 justify-center mt-1">
                  닉네임{" "}
                </div>
                <div className="flex w-1/2 bg-gray-400 p-1 m-1 justify-center">
                  {nickname}
                </div>
              </div>
              <div className="flex w-1/2 border-white border-2">
                <div className="flex w-1/2  p-1 justify-center mt-1">지역 </div>
                <div className="flex w-1/2 bg-gray-400 p-1 m-1 justify-center">
                  {region}
                </div>
              </div>
            </div>
            <div className="flex border-white border-2">
              <div className="p-2 w-1/4 flex justify-center items-center text-2xl">
                능력치
              </div>
              <div className="grid grid-cols-3 gap-1 w-3/4 p-2">
                <div className="bg-gray-400 justify-center flex">
                  체력 : 100
                </div>
                <div className="bg-gray-400 justify-center flex">
                  공격력: {data.attack}
                </div>
                <div className="bg-gray-400 justify-center flex">
                  방어력: {data.defense}
                </div>
                <div className="bg-gray-400 justify-center flex">
                  정확도: {data.accuracy}
                </div>
                <div className="bg-gray-400 justify-center flex">
                  민첩성: 없슈
                </div>
                <div className="bg-gray-400 justify-center flex">
                  무게: {data.weight}
                </div>
              </div>
            </div>
          </div>
          <div className="w-1/4 flex justify-center items-center text-white bg-gray-400 text-6xl">
            10일
          </div>
        </div>
      </div>

      <div className="text-lg font-bold bg-gray-400 w-1/3 flex justify-center rounded-t">
        사망 이력
      </div>
      <div className="bg-gray-400">
        <div className="bg-white m-2 pt-1 pb-1">
          <ul className=" p-2 m-2">
            {[...Array(6)].map((_, i) => (
              <li key={i} className="py-2 px-2  bg-gray-400 m-2 p-2 text-white">
                Day {i + 1}: 내용
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div>
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white py-1 px-4 rounded mt-2"
        >
          다시 시작
        </button>
      </div>
    </div>
  );
};
export default Predict;
