from stable_baselines3 import PPO
from modules.Reinforce_ENV import CustomSurvivalEnv
import os

model_path = os.path.join(os.path.dirname(__file__), 'model', 'Reinforce')

async def run_simulation(population_rate, agent_params, episodes=1):
    # 저장된 모델 불러오기
    model = PPO.load(model_path)
    print(model)
    
    # 환경 재설정
    env = CustomSurvivalEnv(populationRate=population_rate, agent_params=agent_params)

    # 최종 반환 객체 초기화
    simulation_result = {
        "simulate_log": [],         # 모든 에피소드 로그를 하나의 리스트에 저장
        "end_reason": None # 최종 종료 이유를 저장할 필드
    }

    for episode in range(episodes):
        obs, _ = env.reset()
        done = False
        
        while not done:
            action, _states = model.predict(obs)
            obs, reward, done, _, _ = env.step(action)

        # 에피소드 로그와 종료 이유 추가
        simulation_result["simulate_log"].extend(env.logs["log"])  # 각 에피소드의 로그를 하나의 리스트에 추가
        simulation_result["end_reason"] = env.logs["end_reason"]  # 마지막 에피소드의 종료 이유로 업데이트

    return simulation_result