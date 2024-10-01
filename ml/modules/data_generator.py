import tensorflow as tf

def data_generator(
    rotation_range=20, 
    width_shift_range=0.2, 
    height_shift_range=0.2, 
    horizontal_flip=True, 
    zoom_range=0.2, 
    rescale=1.0
    ):
    
    """
    todo 이미지 데이터를 증강시키는 함수입니다.

    * Args:
        ? rotation_range (int): 이미지 회전 각도 범위 (기본값: 20)
        ? width_shift_range (float): 가로 방향으로 이동할 범위 비율 (기본값: 0.2)
        ? height_shift_range (float): 세로 방향으로 이동할 범위 비율 (기본값: 0.2)
        ? horizontal_flip (bool): 수평 뒤집기를 수행할지 여부 (기본값: True)
        ? zoom_range (float): 이미지 확대/축소 범위 비율 (기본값: 0.2)
        ? rescale (float): 이미지 값을 스케일링할 인자 (기본값: 1.0)

    * Returns:
        tf.keras.preprocessing.image.ImageDataGenerator: 설정된 데이터 증강 객체
    """
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=rotation_range,
        width_shift_range=width_shift_range,
        height_shift_range=height_shift_range,
        horizontal_flip=horizontal_flip,
        zoom_range=zoom_range,
        rescale=rescale
    )
    
    return datagen
