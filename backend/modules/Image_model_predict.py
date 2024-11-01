import onnxruntime as ort
from PIL import Image
import numpy as np
from typing import Dict
from fastapi import HTTPException
from modules.static.class_list import class_list
import io

"""
FastAPI 기반 비동기 응답에 대응하는 함수입니다.
  해당 함수는 두 개의 매개변수를 요구합니다.
  처리 과정 중 문제가 발생할 시, FastAPI의 내장 모듈인 HTTPException을 이용해 500 코드의 오류를 반환합니다.
  
  최종적으로, 해당 코드는 다음과 같은 형태의 dict를 반환합니다.
  {
    "species" : 1,
    "attack": "2",
    "defense": "1",
    "accuracy": "61"
    "weight" : "100"
  }
  
  주의 할 점은 모든 반환 값은 float를 이용한 실수가 아닌 int 를 사용한 정수형 입니다.
  
  @img_data:
    서버를 통해 전달된 이미지 바이너리 데이터를 읽어들인 값 입니다.
    
  @model
    model_loader 함수를 이용해 모델의 반환값을 받아냅니다.
"""

async def model_predict(img_data: bytes, model: ort.InferenceSession) -> Dict[str, int]:
    try:
        # 이미지 전처리
        image = Image.open(io.BytesIO(img_data)).convert("RGB")
        image = image.resize((256, 128))  # 모델에 맞게 입력 크기 조정 (필요에 따라 조정 가능)
        image_array = np.array(image).astype("float32") / 255.0
        image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가, (1, 128, 256, 3)

        # ONNX 모델 예측
        input_name = model.get_inputs()[0].name
        predictions = model.run(None, {input_name: image_array})[0]

        # 예측 결과를 dict로 정리
        response = {}
        for i, class_name in enumerate(class_list):
            pred_value = predictions[0][i]  # 2차원 배열 접근 방식 사용

            # 값 변환 및 반올림 후 정수형으로 변환
            if class_name == "species":
                response["species"] = 1 if pred_value >= 0.5 else 0
            else:
                response[class_name] = int(round(pred_value))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")