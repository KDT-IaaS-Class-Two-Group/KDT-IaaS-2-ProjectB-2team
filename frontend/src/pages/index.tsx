import { useState, useEffect } from "react";


interface Response {
  Hello: string;
}

const Hello = () => {
  const [message,setMessage] = useState<Response>({Hello : ""})

  useEffect(()=>{
    const fetchData = async()=>{
      try {
        const res = await fetch('http://127.0.0.1:8000/');
        const data = await res.json()
        setMessage(data)
      } catch (error) {
        console.log(error)
      }
    }
    fetchData()
  },[]);
  
// 클릭 이벤트가 발생하면 콘솔에 숫자 1이 나타나게 
// id = "root"안에 있는 첫번째 div의 id를 찾아서 나타나게 
// 이제 이 id값을 fetch로 위에 http://127.0.0.1:8000으로 보내는 코드를 만든다.
const eventhandle = async () => {
  console.log("1");
  const killingFieldDiv = document.getElementById('killingfield');
  
  if (killingFieldDiv) {
    const idValue = killingFieldDiv.id;
    console.log(idValue); // "killingfield"를 콘솔에 출력합니다.

    // GET 요청 보내기
    try {
      const response = await fetch(`http://127.0.0.1:8000/${idValue}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const responseData = await response.json(); // 응답 데이터 받아오기
      console.log('Response from server:', responseData);
      console.log(responseData.message)
    } catch (error) {
      console.log('Error sending id:', error);
    }
  }
};
  return (
    <div id="root">
      <div id="killingfield">
        <h1>Hello, {message.Hello ? message.Hello : "fail" }, {}</h1>
        <div>
          <button type="button" onClick={eventhandle}>버튼</button>
        </div>
      </div>
    </div>
  );
};

export default Hello;
