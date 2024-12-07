/**
 * StatCard에서 사용하는 인터페이스입니다.
 * img의 경우 컨텍스트에 올라가있는 이미지르 사용하고 있기 때문에 Omit 유틸리티 타입을 이용해서 img 를 제거한 새로운 타입을 선언합니다.
 * Props 로 전달되는 데이터의 경우, 중첩된 객체 형식을 활용하고 있기 때문에 해당 형식에 맞춰 인터페이스를 구성했습니다. 
*/

import { ISubmitData, IStat } from "@/shared/interface/data.interface";

export interface IStatCard {
  userData: Omit<ISubmitData, "img">;
  stat: IStat;
}
