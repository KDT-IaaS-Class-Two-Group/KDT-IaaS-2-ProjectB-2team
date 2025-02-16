import os
import onnxruntime as ort
import numpy as np
from modules.Reinforce_ENV import CustomSurvivalEnv

# ONNX 모델 로드
model_path = os.path.join(os.path.dirname(__file__), 'model', 'ReinforceModel.onnx')
ort_session = ort.InferenceSession(model_path)

async def run_simulation(population_rate, agent_params, episodes=1):
    # 환경 재설정
    env = CustomSurvivalEnv(populationRate=population_rate, agent_params=agent_params)

    # 최종 반환 객체 초기화
    simulation_result = {
        "simulate_log": [],
        "end_reason": None
    }

    for episode in range(episodes):
        obs, _ = env.reset()
        done = False

        while not done:
            # ONNX 모델 예측 수행 (PyTorch 없이 실행)
            obs = np.array(obs, dtype=np.float32).reshape(1, -1)  # 입력 데이터 변환
            inputs = {"obs": obs}  # ONNX 입력 데이터 구조
            action = ort_session.run(["action"], inputs)[0]  # ONNX 기반 예측
            
            obs, reward, done, _, _ = env.step(action)

        # 에피소드 로그와 종료 이유 추가
        simulation_result["simulate_log"].extend(env.logs["log"])
        simulation_result["end_reason"] = env.logs["end_reason"]

    return simulation_result