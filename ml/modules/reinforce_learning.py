import gymnasium as gym  # Gym 대신 Gymnasium을 사용
from gymnasium import spaces
import numpy as np
import math

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
        """
        환경을 초기화하는 생성자 메서드입니다.
        populationRate: 인구 밀도에 따라 환경의 초기 값을 설정합니다.
        """
        super(CustomSurvivalEnv, self).__init__()

        # 상태 공간 정의: HP, 공격력, 방어력, 정확도, 체중, 민첩성
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0]), 
                                            high=np.array([100, 10, 10, 100, 200, 10]), 
                                            dtype=np.float32)
        # 행동 공간 정의: 탐색(0), 휴식(1)
        self.action_space = spaces.Discrete(2)

        self.populationRate = populationRate  # 인구 밀도 설정
        self.state = None
        self.food = None
        self.risk_factor = None
        self.reset()

    def reset(self, seed=None, options=None):
        """
        환경을 초기 상태로 재설정합니다. 이 메서드는 매 에피소드가 시작될 때 호출됩니다.
        """
        super().reset(seed=seed)  # Gymnasium에서 seed를 사용하여 재설정할 수 있습니다.

        self.state = {
            "hp": np.random.randint(50, 101),  # 초기 체력: 50~100 사이의 무작위 값
            "attack": np.random.uniform(1.0, 3.0),  # 초기 공격력
            "defense": np.random.uniform(1.0, 3.0),  # 초기 방어력
            "accuracy": np.random.randint(50, 101),  # 초기 정확도
            "weight": np.random.uniform(50, 150),  # 초기 체중
            "agility": np.random.uniform(0, 10)   # 초기 민첩성
        }

        # 식량 분포: 인구 밀도에 따라 식량을 결정합니다.
        self.food = 100 * (1 + self.populationRate / 100)

        # 위험 요소: 시그모이드 함수를 사용하여 위험 요소의 조우 확률을 설정합니다.
        self.risk_factor = self.calculate_risk_factor(self.populationRate)

        return np.array(list(self.state.values()), dtype=np.float32), {}  # Gymnasium에서는 (obs, info) 형태로 반환

    def calculate_risk_factor(self, populationRate):
        """
        시그모이드 함수를 사용하여 위험 요소의 조우 확률을 계산합니다.
        populationRate: 인구 밀도에 기반한 위험 요소를 결정합니다.
        """
        return 1 / (1 + math.exp(-0.1 * (populationRate - 50)))

    def step(self, action):
        """
        에이전트가 환경에서 한 행동에 대한 결과를 처리하고, 새로운 상태와 보상을 반환합니다.
        action: 에이전트가 수행한 행동 (0: 탐색, 1: 휴식)
        """
        success = False  # 탐색 성공 여부 초기화

        # 행동에 따른 결과 처리
        if action == 0:  # 탐색
            success = np.random.rand() > self.risk_factor  # 위험 요소와의 조우 여부 결정
            if success:
                self.food += 1  # 성공적으로 탐색 시 식량 추가
        elif action == 1:  # 휴식
            self.state["hp"] = min(100, self.state["hp"] + 10)  # 휴식 시 체력 회복

        # 보상 함수 계산
        reward = self.calculate_reward(action, success)

        # 종료 조건: HP가 0이 되거나 식량이 모두 소진된 경우
        done = self.state["hp"] <= 0 or self.food <= 0
        truncated = False  # Gymnasium에서는 truncated 값을 추가해야 합니다.

        new_state = np.array(list(self.state.values()), dtype=np.float32)  # 새로운 상태 반환
        return new_state, reward, done, truncated, {}  # Gymnasium에서는 (obs, reward, done, truncated, info) 형태로 반환

    def calculate_reward(self, action, success):
        """
        보상 함수를 사용하여 에이전트의 행동에 따른 보상을 계산합니다.
        action: 에이전트가 수행한 행동
        success: 탐색의 성공 여부
        """
        reward = 1  # 하루를 살아남았을 때 기본 보상

        # 탐색 행동에 대한 보상 및 페널티 설정
        if action == 0:  # 탐색
            if success:
                reward += 10 + (self.risk_factor * 10)  # 위험도가 높을수록 더 큰 보상
            else:
                reward -= 10 + (self.risk_factor * 5)  # 실패 시 페널티
        elif action == 1:  # 휴식
            reward += 2 if self.state["hp"] < 50 else 1  # 체력이 낮을 때 휴식 보상 증가

        # 식량 감소에 따른 페널티
        self.food -= 1  # 하루가 지나갈 때마다 식량 1 감소
        if self.food <= 0:
            reward -= 10  # 식량이 없을 때 페널티
            self.state["agility"] = max(0, self.state["agility"] - 0.5)  # 민첩성 감소
            self.state["hp"] = max(0, self.state["hp"] - 1)  # HP 감소

        return reward

    def render(self, mode='human'):
        """
        현재 상태와 관련 정보를 화면에 출력합니다.
        """
        print(f"State: {self.state}, Food: {self.food}, Risk Factor: {self.risk_factor}")

    def close(self):
        """
        환경 종료 시 호출됩니다.
        """
        pass
