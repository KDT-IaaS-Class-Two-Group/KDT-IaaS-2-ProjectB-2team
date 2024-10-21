from stable_baselines3 import PPO
from modules.Reinforce_ENV import CustomSurvivalEnv

env = CustomSurvivalEnv()

model = model = PPO('MlpPolicy', env, verbose=1, learning_rate=0.0001, n_steps=2048, batch_size=128, n_epochs=20, gamma=0.99)
model.learn(total_timesteps=200000)

model.save("ppo_model")

import torch.onnx

dummy_input = env.observation_space.sample()
dummy_input = torch.tensor(dummy_input, dtype=torch.float32).unsqueeze(0)

torch.onnx.export(
    model.policy,
    dummy_input,
    "ppo_model.onnx",
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['output']
)

print("ONNX 모델이 성공적으로 생성되었습니다.")
