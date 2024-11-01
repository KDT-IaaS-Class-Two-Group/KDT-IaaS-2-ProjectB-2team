import torch
from stable_baselines3 import PPO

"""
    사전에 학습시킨 PPO 모델의 정책 네트워크를 추출해서 저장하는 함수입니다.
    이 함수를 이용해서 제작된 파일은 별도의 환경 정의 파일과 같이 이용해야 합니다.
    
    model_path
        변환할 모델의 경로입니다.
        
    output_name
        제작될 모델의 이름입니다.
        
    return
    None
"""

def PPO_model_convert(model_path : str , output_name : str) -> None :
    
    model = PPO.load(model_path)

    # 학습된 모델의 정책 네트워크를 ONNX로 변환
    dummy_input = torch.randn(1, model.policy.observation_space.shape[0], dtype=torch.float32)

    # 정책 네트워크만 ONNX로 내보냄
    torch.onnx.export(
        model.policy,                # 정책 네트워크만 변환
        dummy_input,                 # 환경 관측 공간의 더미 입력
        f"{output_name}.onnx",           # ONNX로 저장할 파일명
        export_params=True,          # 학습된 가중치 포함
        opset_version=11,            # ONNX opset 버전
        input_names=["input"],       # 입력 이름 정의
        output_names=["output"]      # 출력 이름 정의
    )

    print(f"{output_name}.onnx 로 파일이 생성되었습니다.")


# 실행 예시
if __name__ == "__main__":
    
    model_path = "여기에 변환할 모델의 경로를 입력해주세요"
    output_name = "내보낼 정책 파일의 이름을 입력해주세요"
    PPO_model_convert(model_path, output_name)