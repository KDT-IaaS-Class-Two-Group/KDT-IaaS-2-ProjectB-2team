import json
import tensorflow as tf


imglocation = "./images/hamdy-abdelwahab.png"


def imageDataNormalize(image_path, save_file_name = "image.normalize.json", resize = (128,256)):
 
    """
    todo 이미지를 정규화 한 데이터를 시각화 하는 함수입니다. 이 함수를 통해 전처리 및 정규화 된 이미지는 json Array 형식으로 저장됩니다.

    * Args:
        ? img_path
        함수를 통해 정규화 할 이미지의 경로

        ? resize
        이미지 크기를 재조정 하기 위한 튜플입니다. (weight, height)으로 이루어져 있으며 기본값은 128,256 입니다
        
        ? save_file_name
        전처리 된 이미지를 저장할 때 사용할 파일 이름입니다. 기본값은 'image.normalize.json'입니다.

    * Return
        None
    """
    
    images_preprocessed = []

    img_process = tf.keras.preprocessing.image

    img = img_process.load_img(image_path, target_size=resize)  # 이미지 크기 조정
    img_array = img_process.img_to_array(img) / 255.0  # 정규화

    images_preprocessed.append(img_array.tolist())

    with open(save_file_name, 'w', encoding='utf-8') as outfile:
        json.dump(images_preprocessed, outfile, ensure_ascii=False, indent=4)

    print(f"Preprocessed image data has been saved. file name : {save_file_name}")
