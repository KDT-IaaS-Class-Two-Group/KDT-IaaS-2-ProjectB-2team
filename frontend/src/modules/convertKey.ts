import statTable from "@/shared/StatTable";

const convertKey = (key: string): string => {
  return statTable[key] || key; // keyMap에 없으면 원래 키 반환
};

export default convertKey;