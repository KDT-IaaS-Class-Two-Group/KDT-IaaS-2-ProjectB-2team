import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      screens: {
        fhd: "1920px",
      },
      colors: {
        baseBg: "#332F47CC", // 기본 배경색
        hoverText: "#FF5733", // hover 시 텍스트 색상
      },
      fontFamily: {
        cfont: ["cfont", "sans-serif"],
      },
      animation: {
        blink: "blink 2.5s infinite", // 애니메이션 이름 및 설정
      },
      keyframes: {
        blink: {
          "0%, 100%": {
            backgroundColor: "var(--tw-bg-opacity, #332F47CC)", // 초기 배경색
            color: "white", // 초기 텍스트 색상
          },
          "50%": {
            backgroundColor: "var(--tw-bg-opacity, #6a5abc96)", // 조정된 배경색
            color: "var(--tw-hoverText, #FF5733)", // 변경된 텍스트 색상
          },
        },
      },
    },
  },
  plugins: [],
};

export default config;