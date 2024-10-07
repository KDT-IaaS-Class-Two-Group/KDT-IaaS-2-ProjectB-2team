import gymnasium as gym
from stable_baselines3 import PPO
from modules.reinforce_learning import CustomSurvivalEnv  # 우리가 정의한 환경을 임포트
import matplotlib.pyplot as plt

# 1. 환경 초기화
env = CustomSurvivalEnv(populationRate=50)

# 2. PPO 알고리즘 초기화
model = PPO('MlpPolicy', env, verbose=1, learning_rate=0.0001, n_steps=2048, batch_size=128, n_epochs=20, gamma=0.99)

# 3. 에이전트 학습 시작
model.learn(total_timesteps=200000)

# 4. 학습된 모델 저장
model.save("ppo_custom_survival_model2")

# 5. 학습된 모델 로드 및 평가
loaded_model = PPO.load("ppo_custom_survival_model2")

# 시뮬레이션 실행 및 보상 기록
total_rewards = []  # 에피소드별 총 보상을 기록하기 위한 리스트
num_episodes = 100  # 실행할 총 에피소드 수

for episode in range(num_episodes):
    obs, info = env.reset()  # Gymnasium에서는 reset() 함수가 (obs, info)를 반환합니다.
    done = False
    episode_reward = 0  # 현재 에피소드의 보상

    while not done:
        action, _states = loaded_model.predict(obs)
        obs, reward, done, _, info = env.step(action)  # step() 함수도 (obs, reward, done, truncated, info)를 반환합니다.
        episode_reward += reward  # 에피소드 보상 누적
        env.render()

    total_rewards.append(episode_reward)  # 에피소드가 끝날 때 총 보상 저장

# 6. 학습 결과 시각화
plt.plot(total_rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Total Reward per Episode during Training')
plt.show()
