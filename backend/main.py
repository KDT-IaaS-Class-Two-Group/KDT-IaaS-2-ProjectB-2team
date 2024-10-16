from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import uvicorn
import json
import os
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict,List
import base64
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
        response = {class_list[i]: int(predictions[0][i]) for i in range(len(class_list))}

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
        
# M2 함수 정의
async def M2(nickname: str, predictions: Dict[str, int], temp_array_1: List, temp_array_2: List) -> Dict:
    result = {
        "nickname": nickname,
        "stat": predictions,  # M1 모델의 예측 결과
        "log": [temp_array_1, temp_array_2]  # 두 개의 임시 배열
    }
    # 결과를 잘 보이게 출력
    print("M2 함수 호출 결과:", result)
    return result

# 임시 저장 객체 (예시로 dict 사용)
temp_storage = {}

@app.post("/result")
async def upload_and_predict(
    nickname: str = Form(...),
    region: str = Form(...),
    img: UploadFile = File(...)
):
    try:
        # 이미지 파일을 바이너리 데이터로 읽기
        img_data = await img.read()

        # 임시 객체에 데이터 저장
        temp_obj = TempData(nickname=nickname, region=region, img_data=img_data)
        temp_storage[nickname] = temp_obj  # nickname을 키로 사용하여 저장

        # 저장된 데이터를 print로 출력
        # print(f"Nickname: {temp_obj.nickname}")
        # print(f"Region: {temp_obj.region}")
        # print(f"Image Data (binary): {temp_obj.img_data[:10]}... (truncated)")  # 이미지 데이터는 일부만 출력

        # 모델 예측 수행
        response = await model_predict(temp_obj.img_data, model)

        # M2 함수 호출 (임시 배열을 설정)
        temp_array_1 = [{} for _ in range(9)]  # 임시 배열 9개 생성
        temp_array_2 = [{} for _ in range(9)]
        result = await M2(temp_obj.nickname, response, temp_array_1, temp_array_2)
        img_trans =  base64.b64encode(temp_obj.img_data).decode("utf-8")
        # 최종 반환할 결과값
        final_result = {
            "result": {
                "nickname": temp_obj.nickname,
                "img": img_trans,  # 이미지 바이너리 데이터 => 디코딩 필요
                "region": temp_obj.region,
                "stat": result["stat"],  # 모델 예측 결과
                "log": result["log"]  # 임시 배열 로그
            }
        }

        # 결과를 콘솔에 출력
        print(final_result)

        # 결과를 클라이언트에게 반환
        return final_result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction and result processing failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)