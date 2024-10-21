import tensorflow as tf
from typing import Dict
from fastapi import HTTPException
from modules.static.class_list import class_list

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


async def model_predict(img_data: bytes, model) -> Dict[str, float]:
    try:
        image = tf.image.decode_image(img_data, channels=3) 
        image = tf.image.resize(image, [128, 256])
        image = tf.expand_dims(image, axis=0)
        image = image / 255.0

        # 3. 모델 예측
        predictions = model.predict(image)

        response = {}
        for i in range(len(class_list)):
            pred_value = predictions[0][i]

            if class_list[i] == 'species':
                response['species'] = 1 if pred_value >= 0.5 else 0
            else:
                response[class_list[i]] = int(round(pred_value, 1))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")