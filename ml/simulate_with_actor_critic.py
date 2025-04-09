import torch
import numpy as np
from torch.distributions import Categorical
from modules.custom_env_ver2 import CustomSurvivalEnv  # 사용자 정의 환경 불러오기
from PPO_learning_ver2 import ActorCritic  # 학습에 사용된 ActorCritic 클래스 불러오기

# 시뮬레이션 설정
MODEL_PATH = "ppo_model.pth"
EPISODES = 3
POPULATION_RATE = 20
AGENT_PARAMS = {
    "species": 0,
    "attack": 2.5,
    "defense": 2.0,
    "accuracy": 80,
    "weight": 120
}
MAX_STEPS = 500

# 환경 초기화
env = CustomSurvivalEnv(populationRate=POPULATION_RATE, agent_params=AGENT_PARAMS)
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

# 모델 로드
model = ActorCritic(state_dim, action_dim)
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

# 시뮬레이션 실행
for ep in range(EPISODES):
    obs, _ = env.reset()
    done = False
    total_reward = 0
    step = 0

    print(f"\n🌿 [에피소드 {ep+1} 시작]")

    while not done and step < MAX_STEPS:
        state_tensor = torch.FloatTensor(obs).unsqueeze(0)
        with torch.no_grad():
            action_probs, _ = model(state_tensor)
        dist = Categorical(action_probs)
        action = dist.sample().item()

        obs, reward, done, _, _ = env.step(action)
        total_reward += reward
        step += 1

    print(f"✅ 생존 턴 수: {step}, 총 보상: {total_reward}")
    env.render()
    print("🧾 로그 종료\n")