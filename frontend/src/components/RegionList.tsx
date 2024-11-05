import { regionList } from "@/shared/static.regionList";
import React from "react";

interface RegionListProps {
  selectedOption: string;
  onSelectChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
}

const RegionList: React.FC<RegionListProps> = ({ selectedOption, onSelectChange }) => {
  return (
    <div className="w-full flex justify-around sm:justify-start bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont">
      <label htmlFor="region" className="text-[#C5C1C3] font-cfont">지역 : </label>
      <select
        id="region"
        value={selectedOption}
        onChange={onSelectChange}
        className="bg-[#332F47CC] text-[#C5C1C3]"
      >
        <option value="선택" className="font-cfont text-[#C5C1C3] text-lg">선택하세요</option>
        {regionList.map((region) => (
          <option key={region} value={region} className="font-cfont text-[#C5C1C3] text-lg">
            {region}
          </option>
        ))}
      </select>
    </div>
  );
};

export default RegionList;