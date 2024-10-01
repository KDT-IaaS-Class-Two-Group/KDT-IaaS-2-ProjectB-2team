import tensorflow as tf
from typing import List, Tuple

def preprocess_image(img_path: str, target_size : Tuple[int,int]=(128, 256)) -> tf.Tensor:
    """
    todo 주어진 경로의 이미지를 읽고, 크기 조정 및 정규화를 수행하는 함수입니다.

    * Args:
        ? img_path (str): 이미지 파일 경로
        ? target_size (tuple, optional): 이미지 크기 조정 (width, height), 기본값 (128, 256)

    * Returns:
        tf.Tensor: 전처리된 이미지 텐서
    """
    
    img_process = tf.keras.preprocessing.image
    img = img_process.load_img(img_path, target_size=target_size)
    img_array = img_process.img_to_array(img) / 255.0  # 정규화
    
    return img_array
