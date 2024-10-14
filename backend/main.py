from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import uvicorn
import json
import os
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI()
class_list = ["species", "attack", "defense", "accuracy", "weight"]

def load_model(model_path: str):
    return tf.keras.models.load_model(model_path)

# 모델 예측 함수
async def model_predict(img_data: bytes, model) -> Dict[str, float]:
    try:
        # 1. 이미지 바이너리 데이터 읽기
        image = tf.image.decode_image(img_data, channels=3)  # RGB 이미지 디코딩
        image = tf.image.resize(image, [128, 256])  # 모델 입력 크기에 맞게 크기 조정
        image = tf.expand_dims(image, axis=0)  # 배치 차원 추가
        image = image / 255.0  # 정규화 (픽셀 값을 0~1 사이로)

        # 3. 모델 예측
        predictions = model.predict(image)

        # 4. JSON 형식으로 응답
        response = {class_list[i]: float(predictions[0][i]) for i in range(len(class_list))}

        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# CORS 설정    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 학습된 모델을 앱 시작 시 한 번만 로드
model = load_model("./model/M5.keras")

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

@app.post("/result")
async def upload_data(
    nickname: str = Form(...),
    region: str = Form(...),
    img: UploadFile = File(...)
):
    # 이미지 파일을 바이너리 데이터로 읽기
    img_data = await img.read()
    
    # 임시 객체에 데이터 저장
    temp_obj = TempData(nickname=nickname, region=region, img_data=img_data)
    temp_storage[nickname] = temp_obj  # nickname을 키로 사용하여 저장

    # 저장된 데이터를 print로 출력
    print(f"Nickname: {temp_obj.nickname}")
    print(f"Region: {temp_obj.region}")
    print(f"Image Data (binary): {temp_obj.img_data[:10]}... (truncated)")  # 이미지 데이터는 일부만 출력
    return {"message": "Data received", "nickname": nickname, "region": region}

@app.post("/predict")
async def predict():
    try:
        # 임시 저장소에서 첫 번째 객체 가져오기
        if not temp_storage:
            raise HTTPException(status_code=400, detail="No image data available")

        # temp_storage의 첫 번째 TempData 객체를 가져와
        temp_obj = next(iter(temp_storage.values()))  # 첫 번째 저장된 객체를 가져옴
        img_data = temp_obj.img_data  # 저장된 이미지 데이터 가져오기

        # model_predict 함수를 호출하여 예측 결과를 가져옴
        response = await model_predict(img_data, model)  # img_data를 직접 전달
        print(response)
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
