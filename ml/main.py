import tensorflow as tf
import numpy as np
from PIL import Image

# 클래스 이름 리스트 (예: 공격력, 방어력 등)
class_list = ["species", "attack", "defense", "accuracy", "weight"]

# 미리 학습된 모델 로드
def load_model(model_path):
    return tf.keras.models.load_model(model_path)

# 모델 예측 함수
def model_predict(image_path, model):
    try:
        # 1. 이미지 파일 열기
        image = Image.open(image_path)

        # 2. 이미지가 RGBA(알파 채널)이면 RGB로 변환
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # 3. 이미지 전처리: (256, 128) 크기로 리사이즈
        image = image.resize((256, 128))  # 모델 입력 크기로 조정 (세로 128, 가로 256)
        image = np.array(image)  # 이미지 데이터를 numpy 배열로 변환
        image = image / 255.0  # 정규화 (0~1 사이의 값으로 변환)
        image = np.expand_dims(image, axis=0)  # 배치 차원 추가

        # 4. 모델 예측
        predictions = model.predict(image)

        response = {}
        for i in range(len(class_list)):
            pred_value = predictions[0][i]

            # species 값 처리 (0.5 이상은 1로, 그 미만은 0으로)
            if class_list[i] == 'species':
                response['species'] = 1 if pred_value >= 0.5 else 0
            else:
                response[class_list[i]] = int(round(pred_value, 1))  # 다른 값은 반올림 후 정수 변환

        return response
    
    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        return None

# 실행 예시
if __name__ == "__main__":
    # 모델 경로 및 이미지 경로
    model_path = "./model/M5.keras"  # 실제 모델 파일 경로
    image_path = "./data/test.png"  # 예측할 이미지 경로

    # 미리 학습된 모델 로드
    model = load_model(model_path)

    # 모델 예측
    result = model_predict(image_path, model)

    if result:
        print("Prediction result:", result)
    else:
        print("Prediction failed.")
