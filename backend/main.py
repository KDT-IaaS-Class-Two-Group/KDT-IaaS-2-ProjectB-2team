from fastapi import FastAPI, File, Form, UploadFile
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
# 임시 객체 구조체
class TempData:
    def __init__(self, nickname: str, region: str, img_data: bytes):
        self.nickname = nickname
        self.region = region
        self.img_data = img_data

# 임시 저장 객체 (예시로 dict 사용)
temp_storage = {}
# 현재 파일이 실행되는 디렉토리 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

# 'data' 폴더 하위의 'data.json' 파일 경로 동적으로 생성
file_path = os.path.join(current_dir, 'data', 'data.json')

# 파일 열기
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 파일을 파싱해서 Python 객체로 변환
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/{get_end_point}")
# def dynamic_get(get_end_point: str):
#     return {"message": f"Hello from {get_end_point}"}
# @app.post("/{post_end_point}")
# def dynamic_get(post_end_point: str):
#     return {"message":data}

# /result 엔드포인트 생성
# @app.post("/result")
# async def receive_result(
#     nickname: str = Form(...),
#     region: str = Form(...),
#     img: bytes = File(...)  # 바이너리 데이터를 바로 받음
# ):
#     dto = ResultDTO(nickname=nickname, region=region)  # DTO로 텍스트 데이터 처리
    
#     # img는 bytes로 받아지며, 그대로 파일로 저장하거나 사용할 수 있음.
#     img_size = len(img)
    
#     return {
#         "nickname": dto.nickname,
#         "region": dto.region,
#         "filesize": img_size
#     }
@app.post("/result")
# async def result(nickname: str = Form(...), region: str = Form(...), img: UploadFile = File(...)):
#     print({"nickname": nickname, "region": region, "filename": img.filename})
#     # 파일을 처리하는 코드 (파일명 반환 예시)
#     return {"nickname": nickname, "region": region, "filename": img.filename}
async def upload_data(
    nickname: str = Form(...),
    region: str = Form(...),
    img: UploadFile = File(...)
):
    # 이미지 파일을 바이너리 데이터로 읽기
    img_data = await img.read()
    
    # 임시 객체에 데이터 저장
    temp_obj = TempData(nickname=nickname, region=region, img_data=img_data)
    temp_storage[nickname] = temp_obj  # 예시로 nickname을 키로 사용
    # 저장된 데이터를 print로 출력
    print(f"Nickname: {temp_obj.nickname}")
    print(f"Region: {temp_obj.region}")
    print(f"Image Data (binary): {temp_obj.img_data[:10]}... (truncated)")  # 이미지 데이터는 일부만 출력
    return {"message": "Data received", "nickname": nickname, "region": region}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)