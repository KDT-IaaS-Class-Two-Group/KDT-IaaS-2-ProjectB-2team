// pages/_app.tsx
import React from 'react';
import { AppProps } from 'next/app';
import { UserProvider } from '@/components/context';

const App: React.FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <UserProvider>
      <Component {...pageProps} />
    </UserProvider>
  );
};

export default App;
