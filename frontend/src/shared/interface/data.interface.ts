/**
 * 전체 데이터에 대한 인터페이스 일반입니다.
 */

//* userpage 컴포넌트에서 사용자가 입력하는 데이터에 대한 인터페이스 입니다.
export interface ISubmitData {
  nickname : string,
  region : string,
  img : string,
}

//* 서버에서 반환되는 데이터 인터페이스 입니다.
export interface IResultData {
  stat: IStat,
  log : ILog
}

export interface IStat {
  health : number;
  species : number;
  attack: number;
  defense: number;
  accuracy: number;
  weight: number;
  agility : number
}

export interface ILog {
  simulate_log: ISimulate_log[];
  end_reason: string;
}
/**
 * 백엔드 서버에서 강화 학습 모델이 산출해내는 예측치에 대한 인터페이스 입니다. 
 * 객체 내에 key값이 모델이 산출해내는 예측 값 만클 늘어납니다.
*/
export interface ISimulate_log {
  [day : string] : string[]
}