import tensorflow as tf
import matplotlib.pyplot as plt

def visualize_weight_bias(model_path : str):
    
    """
    todo 학습된 모델 파일의 가중치와 편향치 분포를 그래프로 표시해주는 함수입니다.
    사전에 학습이 완료된 모델 파일이 필요합니다.
    
    * Arg:
      ? model_path
      모델 파일의 경로입니다.
      
    """

    model = tf.keras.models
    model_file = model.load_model(model_path)
    model_name = model_path.split('.')[0]

    # 모든 레이어의 가중치와 편향 정보 가져오기
    weights = model_file.get_weights()

    # 전체 레이어의 가중치와 편향 분포 시각화
    num_layers = len(weights) // 2  # 가중치와 편향이 한 쌍씩 있으므로 총 레이어 수는 weights의 절반

    plt.figure(figsize=(15, 5 * num_layers))  # 그래프 크기 조정

    for layer_num in range(num_layers):
        # 각 레이어의 가중치와 편향을 가져옴
        layer_weights = weights[layer_num * 2]      # 가중치
        layer_bias = weights[layer_num * 2 + 1]     # 편향
        
        # 가중치 분포 시각화
        plt.subplot(num_layers, 2, layer_num * 2 + 1)  # 서브플롯 생성
        plt.hist(layer_weights.flatten(), bins=50)
        plt.title(f'{model_name} Layer No.{layer_num + 1} Weight Distribution')
        plt.xlabel('Weight Value')
        plt.ylabel('Frequency')
        
        # 편향 분포 시각화
        plt.subplot(num_layers, 2, layer_num * 2 + 2)  # 서브플롯 생성
        plt.hist(layer_bias.flatten(), bins=50)
        plt.title(f'{model_name} Layer No.{layer_num + 1} Bias Distribution')
        plt.xlabel('Bias Value')
        plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()
