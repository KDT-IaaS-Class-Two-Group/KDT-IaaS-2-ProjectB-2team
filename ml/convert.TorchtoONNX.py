import torch
from stable_baselines3 import PPO

# 기존 환경을 이용해 학습된 모델을 불러옵니다.
model = PPO.load("ppo_model")

# 학습된 모델의 정책 네트워크를 ONNX로 변환
dummy_input = torch.randn(1, model.policy.observation_space.shape[0], dtype=torch.float32)

# 정책 네트워크만 ONNX로 내보냄
torch.onnx.export(
    model.policy,                # 정책 네트워크만 변환
    dummy_input,                 # 환경 관측 공간의 더미 입력
    "ppo_policy.onnx",           # ONNX로 저장할 파일명
    export_params=True,          # 학습된 가중치 포함
    opset_version=11,            # ONNX opset 버전
    input_names=["input"],       # 입력 이름 정의
    output_names=["output"]      # 출력 이름 정의
)

print("정책 네트워크가 ONNX 형식으로 성공적으로 변환되었습니다.")
