import json
from typing import List, Optional


def key_gen(json_path : str, remove_key : Optional[str]=None) -> List[str]:
    """
    todo JSON 파일에서 특정 키를 제거한 나머지 키를 추출하는 함수입니다. remove_key의 값이 전달되지 않으면 json 데이터의 모든 key 값을 반환합니다.

    * Args:
        ? json_path (str): JSON 파일의 경로
        ? remove_key (str): 제거할 키의 이름

    * Returns:
        List[str]: 제거된 키를 제외한 나머지 키 목록
    """
    try:
        with open(json_path, "r") as f:
            json_data = json.load(f)
            
        class_list = [key for key in json_data[0] if key != remove_key]
        
        print(class_list)
        
        return class_list
    
    except FileNotFoundError:
        
        print(f"입력하신 파일을 찾을 수 없습니다 : {json_path}")
        return []



# json_path = 'athletes_data.json'
# key_gen(json_path)