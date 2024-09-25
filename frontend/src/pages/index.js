export async function getServerSideProps() {
  // 백엔드 서버에서 /data 엔드포인트로 GET 요청
  const res = await fetch("http://127.0.0.1:8000/"); // 백엔드 서버 URL을 사용하세요
  const data = await res.json();

  return {
    props: {
      message: data.message, // 백엔드에서 가져온 데이터를 props로 전달
    },
  };
}

// pages/hello.js
const Hello = () => {
  return (
    <div id="root">
      <div id="killingfield">
        <h1>Hello,</h1>
      </div>
    </div>
  );
};

export default Hello;
