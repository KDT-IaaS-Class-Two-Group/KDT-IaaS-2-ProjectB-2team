import React, { useState } from "react";
import { IDeathLog } from "./DeathLog.interface";

const ITEMS_PER_PAGE = 10; // 페이지당 항목 수

const DeathLog: React.FC<IDeathLog> = ({ deathLogProps }) => {
  const [page, setPage] = useState(1); // 현재 페이지 상태
  const { simulate_log, end_reason } = deathLogProps;

  // 현재 페이지에 해당하는 데이터 슬라이싱
  const startIndex = (page - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const currentPageLogs = simulate_log.slice(startIndex, endIndex);

  // 총 페이지 수 계산
  const totalPages = Math.ceil(simulate_log.length / ITEMS_PER_PAGE);

  return (
    <div className="flex flex-col justify-between h-3/5 gap-3 p-4 bg-[#332F47CC] rounded border border-[#D9C4B2]">
      {/* Simulation Log */}
      <h2 className="text-lg font-semibold text-[#C5C1C3]">생존 기록</h2>

      <div className="overflow-scroll flex flex-col gap-2">
  {currentPageLogs.map((logEntry: object, index: number) =>
    Object.entries(logEntry).map(([day, events]: [string, string[]]) => (
      <div
        key={index}
        className="border border-[#D9C4B2] p-2 rounded-md bg-[#332F47CC] shadow hover:animate-blink text-white"
      >
        <h3 className="text-sm font-bold">{day}</h3>
        <ul className="list-disc pl-5">
          {events.map((event: string, eventIndex: number) => (
            <li
              key={eventIndex}
              className="text-sm text-[#C5C1C3]"
            >
              {event}
            </li>
          ))}
        </ul>
      </div>
    ))
  )}
</div>

      {/* Pagination Controls */}
      <div className="flex justify-between items-center border border-[#D9C4B2] rounded-md p-2">
        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
          className={`py-1 px-3 rounded ${
            page === 1
              ? "bg-[#7f7f7f] text-gray-700"
              : "bg-[#D9C4B2CC] text-[#332F47CC] hover:bg-[#D9C4B2] hover:text-black"
          }`}
        >
          이전
        </button>
        <p className="text-sm text-[#C5C1C3]">
          Page {page} of {totalPages}
        </p>
        <button
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
          className={`py-1 px-3 rounded ${
            page === totalPages
              ? "bg-[#7f7f7f] text-gray-700"
              : "bg-[#D9C4B2CC] text-[#332F47CC] hover:bg-[#D9C4B2] hover:text-black"
          }`}
        >
          다음
        </button>
      </div>

      {/* End Reason */}
      <div className="mt-4 p-3 border border-[#D9C4B2] rounded-md bg-[#332f476d]">
        <h2 className="text-lg font-semibold text-[#ff4343cc]">사망 원인</h2>
        <p className="text-sm text-[#C5C1C3]">{end_reason}</p>
      </div>
    </div>
  );
};

export default DeathLog;
