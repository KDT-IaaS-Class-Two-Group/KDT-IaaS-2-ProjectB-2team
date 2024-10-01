import tensorflow as tf
from typing import Tuple

def build_model(dropout_rate: float = 0.5, input_shape: Tuple[int, int, int] = (128, 256, 3), output_layer: int = 5) -> tf.keras.Model:
    """
    todo TensorFlow를 이용해 CNN 모델을 생성하는 함수입니다.

    * Args:
        ? dropout_rate (float, optional): 드롭아웃 레이어의 비율로, 과적합을 방지하기 위해 사용됩니다. 기본값은 0.5입니다.
        ? input_shape (Tuple[int, int, int], optional): 입력 이미지의 형태를 나타내는 튜플로, (height, width, channels) 순서로 지정합니다.
            기본값은 (128, 256, 3)으로, 높이 128, 너비 256, RGB 채널 3개를 갖는 이미지를 의미합니다.
        ? output_layer (int, optional): 출력 레이어의 노드 수를 지정하며, 예측하고자 하는 출력 값의 개수입니다. 기본값은 5입니다.

    Returns:
        tf.keras.Model: 구성된 Keras 모델 인스턴스입니다.
    """
    
    layers = tf.keras.layers
    model = tf.keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(dropout_rate), 
        layers.Dense(output_layer)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model
