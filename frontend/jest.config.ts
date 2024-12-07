import type { Config } from "jest";
import nextJest from "next/jest";

const createJestConfig = nextJest({
  dir: "./",
});

const config: Config = {
  testEnvironment: "node", // jsdom 대신 node 환경 사용
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1", // '@/' 별칭 매핑
  },
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },
  testMatch: ["<rootDir>/src/__tests__/**/*.(spec|test).[jt]s?(x)"], // 테스트 파일 경로
};

export default createJestConfig(config);
