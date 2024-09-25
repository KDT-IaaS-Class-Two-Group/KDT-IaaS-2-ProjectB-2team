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
  },[])
  console.log(message)
  console.log(message.Hello)
  
  return (

    <div id="root">
      <div id="killingfield">
        <h1>Hello, {message.Hello ? message.Hello : "fail"}</h1>
      </div>
    </div>
  );
};

export default Hello;
