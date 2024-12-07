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
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      fontFamily: {
        cfont: ["cfont", "sans-serif"],
      },
      /**
       * 커스텀 애니메이션
       * 생존 로그의 div에 마우스 오버 시 반짝이는 애니메이션을 추가
       */
      animation: {
        blink: "blink 2s infinite", // 애니메이션 이름 및 설정
      },
      keyframes: {
        blink: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
    },
  },
  plugins: [],
};

export default config;