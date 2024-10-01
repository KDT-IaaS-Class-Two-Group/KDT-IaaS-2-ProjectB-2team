import matplotlib.pyplot as plt

def visulaize_history(history, title: str = "Model Learning History") -> None:
    """
        todo 학습 및 검증 과정에서의 손실(Loss) 및 평균 절대 오차(MAE)를 시각화하는 함수입니다.

        * Args:
            ? history (keras.callbacks.History): Keras 모델의 학습 과정에서 반환된 History 객체입니다. 
                이 객체에는 'loss', 'val_loss', 'mae', 'val_mae' 등이 포함되어 있어야 합니다.
                
            ? title (str, optional): 그래프의 제목을 지정합니다. 지정하지 않으면 기본 제목으로 표시됩니다.
                기본 제목은 'Model Learning History' 입니다

        * Returns:
            None: 그래프를 화면에 표시합니다.
    """
    plt.figure(figsize=(12, 4))

    # 손실 그래프
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss' if title is None else f'Loss - {title}')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # MAE 그래프
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='Train MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('Mean Absolute Error' if title is None else f'MAE - {title}')
    plt.xlabel('Epochs')
    plt.ylabel('MAE')
    plt.legend()

    plt.tight_layout()
    plt.show()