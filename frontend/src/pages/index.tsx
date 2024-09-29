import { useState, useEffect } from "react";

const Hello = () => {
  const [message,setMessage] = useState<string>("")
  const [message2,setMessage2] = useState<string>("")
  const [message3,setMessage3] = useState<string>("")
  const [message4,setMessage4] = useState<string>("")
  const [message5,setMessage5] = useState<string>("")

  console.log(message);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/');
        const data = await res.json()
        setMessage(data.message)
      } catch (error) {
        console.log(error);
      }
    }
    fetchData()
  },[]);

const eventhandle = async () => {

  console.log("1");

    const killingFieldDiv = document.getElementById("killingfield");

    if (killingFieldDiv) {
      const idValue = killingFieldDiv.id;
      console.log(idValue); // "killingfield"를 콘솔에 출력합니다.

    // GET 요청 보내기
    try {
      const response = await fetch(`http://127.0.0.1:8000/${idValue}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const responseData1 = await response.json(); // 응답 데이터 받아오기

      console.log(responseData1.message.attack)
      setMessage(responseData1.message.attack || "메시지가 없습니다.")
      setMessage2(responseData1.message.defense || "메시지가 없습니다.")
      setMessage3(responseData1.message.accuracy || "메시지가 없습니다.")
      setMessage4(responseData1.message.weight || "메시지가 없습니다.")
      setMessage5(responseData1.message.img || "메시지가 없습니다.")

    } catch (error) {
      console.log('Error sending id:', error);
    }
  }
  
};

console.log(message)
console.log(typeof(message))

  return (
    <div id="root">
      <div id="killingfield">
        <h1>공격력, {message}</h1> 
        <h1>방어력, {message2}</h1>
        <h1>명중률, {message3}</h1>
        <h1>체력, {message4}</h1>
        <h1>이미지, {message5}</h1>
        <div>
          <button type="button" onClick={eventhandle}>
            버튼
          </button>
        </div>
      </div>
    </div>
  );
};

export default Hello;