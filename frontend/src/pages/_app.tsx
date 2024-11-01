// pages/_app.tsx
import React from 'react';
import { AppProps } from 'next/app';
import { UserProvider } from '@/components/context';
import "../../public/globals.css"

const App: React.FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <UserProvider>
      <div className='w-screen h-screen bg'>
        <Component {...pageProps} />
      </div>
    </UserProvider>
  );
};

export default App;
