import React from "react";
import { IDeathLog } from "./DeathLog.interface";

const DeathLog: React.FC<IDeathLog> = ({ deathLogProps }) => {
  const { simulate_log, end_reason } = deathLogProps;

  return (
    <div className="flex flex-col gap-3 p-4 border rounded-lg bg-gray-100">
      {/* Simulation Log */}
      <div className="flex flex-col gap-2">
        <h2 className="text-lg font-semibold text-gray-800">Simulation Log</h2>
        {simulate_log.map((logEntry, logIndex) => (
          Object.entries(logEntry).map(([day, events]) => (
            <div key={`${logIndex}-${day}`} className="border p-2 rounded-md bg-white shadow">
              <h3 className="text-sm font-bold text-gray-600">{day}</h3>
              <ul className="list-disc pl-5">
                {events.map((event: string, index: number) => (
                  <li key={index} className="text-sm text-gray-700">
                    {event}
                  </li>
                ))}
              </ul>
            </div>
          ))
        ))}
      </div>

      {/* End Reason */}
      <div className="mt-4 p-3 border rounded-md bg-red-100">
        <h2 className="text-lg font-semibold text-red-800">End Reason</h2>
        <p className="text-sm text-red-700">{end_reason}</p>
      </div>
    </div>
  );
};

export default DeathLog;