import torch
import numpy as np
from modules.reinforce_learning import CustomSurvivalEnv  # 환경 정의 코드
from models.PPOAgent import PPOAgent  # PPO 에이전트 임포트

def process_image_result(image_result):
    """이미지 인식 결과를 초기 상태로 변환"""
    state = {
        "hp": image_result.get("hp", 100),
        "attack": image_result.get("attack", 2.0),
        "defense": image_result.get("defense", 2.0),
        "accuracy": image_result.get("accuracy", 80),
        "weight": image_result.get("weight", 70),
        "agility": image_result.get("agility", 5.0),
    }
    return np.array(list(state.values()), dtype=np.float32)

def generate_scenario_log(agent, env, initial_state):
    """강화 학습 환경에서 로그를 생성"""
    state = initial_state
    done = False
    day_count = 1
    logs = []  # 시나리오 로그 배열

    while not done:
        # 에이전트가 행동을 선택
        action, _ = agent.select_action(state)

        # 선택한 행동 수행 및 결과 반환
        next_state, reward, done, truncated, _ = env.step(action)

        # 이벤트 로그 작성
        log = create_event_log(day_count, action, reward, env)
        logs.append(log)

        # 상태 전환 및 일자 증가
        state = next_state
        day_count += 1

    # 종료 시 식량이 0일 경우 종료 메시지 추가
    if env.food <= 0:
        logs.append(f"Day {day_count}: 보유하고 있는 식량을 모두 소진했습니다.")

    return logs

def create_event_log(day, action, reward, env):
    """일자별 이벤트 로그를 생성"""
    action_name = "탐색" if action == 0 else "휴식"
    log = f"Day {day}: {action_name}"

    if action == 0:  # 탐색일 때
        if reward > 0:
            log += "에 성공해 음식을 발견했습니다."
        else:
            log += f" 중 위험 요소와 조우하여 HP가 감소했습니다. 현재 HP: {env.state['hp']}"
    elif action == 1:  # 휴식일 때
        log += f"을 통해 체력을 회복했습니다. 현재 HP: {env.state['hp']}"

    # 식량 잔량 정보 추가
    log += f" | 남은 식량: {env.food}"
    return log

if __name__ == "__main__":
    # 이미지 인식 결과 예제
    image_result = {
        "hp": 85,
        "attack": 3.0,
        "defense": 2.5,
        "accuracy": 90,
        "weight": 80,
        "agility": 7.0,
    }

    # 초기 상태 변환
    initial_state = process_image_result(image_result)

    # 환경 및 에이전트 초기화
    env = CustomSurvivalEnv()
    agent = PPOAgent(env.observation_space.shape[0], env.action_space.n)

    # 사전 학습된 모델 로드
    try:
        agent.load_model("models/ppo_model.pth")
        print("모델이 성공적으로 로드되었습니다.")
    except FileNotFoundError as e:
        print(f"모델 파일을 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"모델 로드 중 오류가 발생했습니다: {e}")

    # 시나리오 로그 생성
    scenario_logs = generate_scenario_log(agent, env, initial_state)

    # 로그 출력
    print("시나리오 로그:")
    for log in scenario_logs:
        print(log)
