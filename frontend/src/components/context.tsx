import React, { createContext, useState } from 'react';

interface UserData {
  nickname: string;
  region: string;
  image: string;
  stats: {
    attack: number;
    defense: number;
    accuracy: number;
    weight: number;
  };
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
