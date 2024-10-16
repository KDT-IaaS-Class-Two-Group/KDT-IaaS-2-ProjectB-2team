import React, { createContext, useState } from 'react';

interface UserData {
  result:{
    nickname: string;
    region: string;
    img: string;
    stat: {
      species : number
      attack: number;
      defense: number;
      accuracy: string;
      weight: number;
    },
    log : string[];
  }
}


interface UserContextType {
  userData: UserData | null;
  setUserData: React.Dispatch<React.SetStateAction<UserData | null>>;
}

export const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [userData, setUserData] = useState<UserData | null>(null);

  return (
    <UserContext.Provider value={{ userData, setUserData }}>
      {children}
    </UserContext.Provider>
  );
};
