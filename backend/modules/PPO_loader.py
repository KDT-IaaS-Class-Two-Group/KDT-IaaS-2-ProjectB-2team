from stable_baselines3 import PPO
from modules.Reinforce_ENV import CustomSurvivalEnv
import json
import matplotlib.pyplot as plt


# 저장된 모델 불러오기
model = PPO.load("ppo_custom_survival_model")

# 환경 재설정
env = CustomSurvivalEnv(populationRate=15.5, agent_params={
    "species": 0,
    "attack": 2.5,
    "defense": 2.0,
    "accuracy": 80,
    "weight": 120
})

def run_simulation_and_collect_logs(episodes=5):
    all_logs = []  # 모든 에피소드 로그를 저장할 리스트

    for episode in range(episodes):
        obs, _ = env.reset()  # reset()에서 반환되는 두 번째 값인 info는 무시하고 obs만 사용
        done = False
        episode_logs = []  # 해당 에피소드의 로그를 저장할 리스트
        while not done:
            action, _states = model.predict(obs)  # 저장된 모델로 예측
            obs, reward, done, _, _ = env.step(action)  # 행동을 수행하고 다음 상태로 넘어감

        # 에피소드가 끝나면 로그를 반환
        episode_logs.append(env.logs)  # 각 에피소드의 로그를 수집
        all_logs.append(env.logs)  # 전체 로그에 추가

    return all_logs

# 시뮬레이션 실행 및 로그 수집
logs = run_simulation_and_collect_logs(episodes=1)

# 로그 출력 (요청한 형식으로 JSON 변환)
print("에피소드 로그:")
print(json.dumps(logs, indent=2, ensure_ascii=False))



# 학습 완료 후 테스트 및 보상 데이터 저장
episodes = 100
rewards = []  # 보상 값을 저장할 리스트

for episode in range(episodes):
    obs, _ = env.reset()  # reset()에서 반환되는 두 번째 값인 info는 무시하고 obs만 사용
    done = False
    total_reward = 0
    while not done:
        action, _states = model.predict(obs)  # obs만 전달
        obs, reward, done, _, _ = env.step(action)
        total_reward += reward
    rewards.append(total_reward)  # 각 에피소드의 총 보상을 저장
    print(f"Episode {episode + 1}: Total Reward: {total_reward}")
    
    
    
    
# 보상 그래프 시각화
plt.plot(range(1, episodes + 1), rewards, marker='o')
plt.title("Total Reward per Episode")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.grid(True)
plt.show()
