from fastapi import FastAPI
import uvicorn
import json
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()

#CORS 설정    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# DTO (데이터 전송 객체)
class ResultDTO(BaseModel):
    nickname: str
    region: str
# 현재 파일이 실행되는 디렉토리 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))


# 'data' 폴더 하위의 'data.json' 파일 경로 동적으로 생성
file_path = os.path.join(current_dir, 'data', 'data.json')

# 파일 열기
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 파일을 파싱해서 Python 객체로 변환

print(type(data))
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/{get_end_point}")
# def dynamic_get(get_end_point: str):
#     return {"message": f"Hello from {get_end_point}"}
# @app.post("/{post_end_point}")
# def dynamic_get(post_end_point: str):
#     return {"message":data}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)