import torch
import onnx
from stable_baselines3 import PPO

# 기존 PPO 모델 로드
model_path = "modules/model/Reinforce.zip"  # 기존 PPO 모델 경로
model = PPO.load(model_path)

# 환경의 입력 차원 가져오기
obs_dim = model.observation_space.shape

# 더미 입력 생성 (환경의 상태 차원과 일치해야 함)
dummy_input = torch.randn(1, *obs_dim, dtype=torch.float32)

# ONNX 변환
onnx_model_path = "modules/model/ReinforceModel.onnx"
torch.onnx.export(
    model.policy,  # PPO 모델의 정책 네트워크
    dummy_input, 
    onnx_model_path, 
    input_names=["obs"],  # 기존 1D 벡터 입력 유지
    output_names=["action"], 
    dynamic_axes={"obs": {0: "batch_size"}, "action": {0: "batch_size"}},
    opset_version=11
)

print(f"ONNX 모델이 변환되었습니다: {onnx_model_path}")