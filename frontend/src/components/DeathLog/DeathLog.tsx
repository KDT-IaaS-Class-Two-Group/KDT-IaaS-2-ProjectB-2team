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
    <div className="flex flex-col justify-between h-full gap-3 p-4 border rounded-lg bg-gray-100">
      {/* Simulation Log */}
        <h2 className="text-lg font-semibold text-gray-800">Simulation Log</h2>
      <div className="overflow-scroll flex flex-col gap-2">
        {currentPageLogs.map((logEntry, logIndex) =>
          Object.entries(logEntry).map(([day, events], index: number) => (
            <div
              key={`${logIndex}-${index}`}
              className="border p-2 rounded-md bg-white shadow"
            >
              <h3 className="text-sm font-bold text-gray-600">{day}</h3>
              <ul className="list-disc pl-5">
                {events.map((event: string, eventIndex: number) => (
                  <li key={eventIndex} className="text-sm text-gray-700">
                    {event}
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>

      {/* Pagination Controls */}
      <div className="flex justify-between items-center">
        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
          className={`py-1 px-3 rounded ${
            page === 1 ? "bg-gray-300" : "bg-blue-500 text-white hover:bg-blue-700"
          }`}
        >
          이전
        </button>
        <p className="text-sm text-gray-700">
          Page {page} of {totalPages}
        </p>
        <button
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
          className={`py-1 px-3 rounded ${
            page === totalPages
              ? "bg-gray-300"
              : "bg-blue-500 text-white hover:bg-blue-700"
          }`}
        >
          다음
        </button>
      </div>

      {/* End Reason */}
      <div className="mt-4 p-3 border rounded-md bg-red-100">
        <h2 className="text-lg font-semibold text-red-800">사망 원인</h2>
        <p className="text-sm text-red-700">{end_reason}</p>
      </div>
    </div>
  );
};

export default DeathLog;