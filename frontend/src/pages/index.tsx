// pages/hello.tsx
import { GetServerSideProps } from 'next';

interface HelloProps {
  message: string;
}

export const getServerSideProps: GetServerSideProps = async () => {
  // 백엔드 서버에서 /data 엔드포인트로 GET 요청
  const res = await fetch('http://127.0.0.1:8000/');
  const data = await res.json();

  return {
    props: {
      message: data.message, // 백엔드에서 가져온 데이터를 props로 전달
    },
  };
};

const Hello = ({ message }: HelloProps) => {
  return (
    <div id="root">
      <div id="killingfield">
        <h1>Hello, {message}</h1>
      </div>
    </div>
  );
};

export default Hello;
