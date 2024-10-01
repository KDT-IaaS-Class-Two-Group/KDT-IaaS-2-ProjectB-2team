from fastapi import HTTPException
from typing import Dict
import tensorflow as tf
from .class_list import class_list # class_list 모듈을 제대로 import해야 함

# 모델 예측 함수
async def model_predict(file, model) -> Dict[str, float]:
    try:
        # 1. 이미지 바이너리 데이터 읽기
        image_data = await file.read()

        # 2. TensorFlow로 이미지 처리
        image = tf.image.decode_image(image_data, channels=3)  # RGB 이미지 디코딩
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
