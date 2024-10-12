import React, { useEffect, useState } from 'react';

interface Response {
  species: number;
  attack: string;
  defense: string;
  accuracy: string;
  weight: string;
}


const Predict: React.FC  = () => {
    const [data, setData] = useState<Response | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/result', {
            method: 'POST',
          });
  
          if (!response.ok) {
            throw new Error('서버 응답 오류');
          }
  
          const result = await response.json();
          setData(result.message);
        } catch (error: unknown) {
          if (error instanceof Error) {
            setError(error.message);
          } else {
            setError('알 수 없는 오류가 발생했습니다.');
          }
        } finally {
          setLoading(false);
        }
      };
  
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

  return (
    <div id="root">
      <div>사망보고서</div>
      <div>능력치
        <div>이미지 : {}</div>
        <div>
          <div>
            <div> 
              <div>닉네임</div>
              <div>지역</div>
            </div>
            <div>
              <div>능력치</div>
              <div>
                <div>hp</div>
                <div>공격력 : {data.attack}</div>
                <div>방어력 : {data.defense}</div>
                <div>정확도 : {data.accuracy}</div>
                <div>민첩성 : ?</div>
                <div>무게 : {data.weight}</div>
              </div>
            </div>
          </div>
          <div>10일</div>
        </div>
      </div>
      <div>사망이력</div>
      <div>메인 글 
        <div></div> {/*메인 글은 동적으로 생되게 만들기 */}
      </div>
      <div>버튼</div>
      <div>다음 페이지?</div>
    </div> 
  )
}
export default Predict