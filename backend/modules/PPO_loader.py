import os
import onnxruntime as ort
import numpy as np
from modules.Reinforce_ENV import CustomSurvivalEnv

# ONNX 모델 로드
model_path = os.path.join(os.path.dirname(__file__), 'model', 'ReinforceModel.onnx')
ort_session = ort.InferenceSession(model_path)

# 시뮬레이션 실행 함수
async def run_simulation(population_rate, agent_params, episodes=1, use_model=False):
    simulation_result = {
        "simulate_log": [],
        "end_reason": None
    }

    for episode in range(episodes):
        env = CustomSurvivalEnv(populationRate=population_rate, agent_params=agent_params)
        obs, _ = env.reset()
        done = False

        while not done:
            obs = np.array(obs, dtype=np.float32).reshape(1, -1)

            if use_model:
                # ONNX 모델 기반 예측
                inputs = {"obs": obs}
                action = ort_session.run(["action"], inputs)[0]
                if isinstance(action, np.ndarray):
                    action = int(action.squeeze())  # ndarray → int 변환
            else:
                # 환경 내부 정책 기반 랜덤 액션
                action = env.action_space.sample()

            obs, reward, done, _, _ = env.step(action)

        simulation_result["simulate_log"].extend(env.logs["log"])
        simulation_result["end_reason"] = env.logs["end_reason"]

    return simulation_result