// pages/_app.tsx
import React from "react";
import { AppProps } from "next/app";
import { UserProvider } from "@/components/context";
import "../../public/globals.css";

const App: React.FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <UserProvider>
      <div
        className="bg-center bg-no-repeat bg-contain"
        style={{
          backgroundImage: "url('/images/baseImage.png')",
        }}
      >
        <Component {...pageProps} />
      </div>
    </UserProvider>
  );
};

export default App;
