/**
 * 서버에서 전달되는 key 값을 table 에 기입된 대로 변경을 시도하는 함수입니다.
 * table에 기입되지 않은 key가 들어 온 경우 해당 값을 그대로 반환합니다.
 * @param key 서버에서 전달되는 문자열 key 값입니다.
 * @param table 개발 단에서 지장한 table 객체입니다.
 * @returns table에 해당하는 값이 있을 경우 변환된 문자열이, 그렇지 않은 경우에는 key값이 그대로 통과합니다.
 */

const convertKey = (key: string, table: { [key: string]: string }): string => {
  return table[key] || key; // keyMap에 없으면 원래 키 반환
};

export default convertKey;
