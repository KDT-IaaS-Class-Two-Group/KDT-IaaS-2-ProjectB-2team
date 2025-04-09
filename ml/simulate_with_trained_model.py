import torch
import numpy as np
from torch.distributions import Categorical
from modules.custom_env_ver2 import CustomSurvivalEnv
from PPO_learning2 import PolicyNetwork  # 모델 정의와 동일해야 함

# 모델 경로
MODEL_PATH = "models/ppo_model.pth"

# 시뮬레이션 파라미터
EPISODES = 3
POPULATION_RATE = 25
AGENT_PARAMS = {
    "species": 0,
    "attack": 2.5,
    "defense": 2.0,
    "accuracy": 80,
    "weight": 120
}
MAX_STEPS = 500

# 환경 생성
env = CustomSurvivalEnv(populationRate=POPULATION_RATE, agent_params=AGENT_PARAMS)

# 모델 로드
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
model = PolicyNetwork(state_size, action_size)
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

# 시뮬레이션 실행
for episode in range(EPISODES):
    obs, _ = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done and step_count < MAX_STEPS:
        state = torch.FloatTensor(obs).unsqueeze(0)
        with torch.no_grad():
            action_probs, _ = model(state)
            dist = Categorical(action_probs)
            action = dist.sample().item()

        obs, reward, done, _, _ = env.step(action)
        total_reward += reward
        step_count += 1

    print(f"\n🌿 [에피소드 {episode+1}] 생존 턴 수: {step_count}, 총 보상: {total_reward}")
    env.render()