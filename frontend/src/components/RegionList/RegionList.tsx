import { regionList } from "@/shared/static.regionList";
import RegionListProps from "./RegionList.interface";
import React from "react";



const RegionList: React.FC<RegionListProps> = ({ selectRef }) => {
  return (
    <div className="w-full flex justify-around sm:justify-start bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont">
      <label htmlFor="region" className="text-[#C5C1C3] font-cfont">지역 : </label>
      <select
        id="region"
        ref={selectRef}  // 부모로부터 전달된 ref를 select 요소에 연결
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