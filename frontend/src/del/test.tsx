import { useState } from "react";

interface Response {
	species : number, 
  img: string, 
  attack: string, 
  defense: string, 
  accuracy: string, 
  weight : string
}

const Hello = () => {
  const [message,setMessage] = useState<Response>()

const eventhandle = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/a`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const responseData1 = await response.json(); // 응답 데이터 받아오기
      setMessage(responseData1.message)

    } catch (error) {
      console.log('Error sending id:', error);
    }
  
};

  return (
    <div id="root">
      <div id="killingfield">
        <h1>공격력, {message?.attack}</h1>
        <h1>방어력, {message?.defense}</h1>
        <h1>명중률, {message?.accuracy}</h1>
        <h1>무게, {message?.weight}</h1>
        <h1>이미지, {message?.img}</h1>
        <div>
          <button type="button" onClick={eventhandle}>버튼</button>
        </div>
      </div>
    </div>
  );
};

export default Hello;
