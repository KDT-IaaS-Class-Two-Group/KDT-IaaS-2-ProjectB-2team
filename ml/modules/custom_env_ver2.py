import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
from colorama import Fore, Style, init

# Windows 콘솔을 위한 colorama 초기화
init(autoreset=True)

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50, agent_params=None):
        super(CustomSurvivalEnv, self).__init__()

        # 상태 공간 정의: HP, 공격력, 방어력, 정확도, 체중, 민첩성
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 10, 10, 100, 200, 10], dtype=np.float32),
            dtype=np.float32
        )

        # 행동 공간 정의: 탐색(0), 휴식(1)
        self.action_space = spaces.Discrete(2)

        self.populationRate = populationRate
        self.agent_params = agent_params if agent_params else {
            "species": 0,
            "attack": 1.0,
            "defense": 1.0,
            "accuracy": 50,
            "weight": 50
        }

        self.state = None
        self.food = None
        self.rest_turns = 0
        self.turns_survived = 0
        self.food_acquired = 0
        self.end_reason = ""
        self.food_depletion_days = 0  # 식량 0일 때 경과한 일 수

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        weight = self.agent_params["weight"]

        # 초기 상태 설정
        self.state = {
            "hp": min(100, weight * 0.3),  # 체력 = weight의 0.3배
            "attack": self.agent_params["attack"],
            "defense": self.agent_params["defense"],
            "accuracy": self.agent_params["accuracy"],
            "weight": weight,
            "agility": max(0, 10 - weight * 0.3)  # 민첩성 감소
        }

        self.food = min(10, 10 * (1 + self.populationRate / 100))  # 초기 식량 최대 10
        self.rest_turns = 0
        self.turns_survived = 0
        self.food_acquired = 0
        self.end_reason = ""
        self.food_depletion_days = 0  # 식량 0일 경과 초기화

        return np.array(list(self.state.values()), dtype=np.float32), {}

    def step(self, action):
        self.turns_survived += 1  # 생존 턴 증가
        self.food -= 1  # 매 턴 식량 1 감소

        # 식량이 0일 때 HP 감소 로직
        if self.food <= 0:
            self.food_depletion_days += 1  # 식량 0일 경과 증가
            hp_loss = self.calculate_hp_loss()  # HP 감소량 계산
            self.state["hp"] -= hp_loss
            print(Fore.RED + f"식량이 부족합니다! HP가 {hp_loss} 감소했습니다.")
        else:
            self.food_depletion_days = 0  # 식량이 있으면 경과 일 수 초기화

        success = False

        if action == 0:  # 탐색
            success = np.random.rand() > self.calculate_risk_factor()
            if success:
                self.handle_exploration_success()
            else:
                self.handle_exploration_failure()

        elif action == 1:  # 휴식
            if self.state["hp"] < 100:
                self.handle_rest()

            self.rest_turns += 1  # 연속 휴식 카운트 증가
            if self.rest_turns > 2 and np.random.rand() < 0.3:
                print(Fore.RED + "휴식 중에 위험 요소가 침입했습니다!")
                self.handle_exploration_failure()

        reward = self.calculate_reward()  # 생존 일자 기준 보상
        done = self.check_done()

        return np.array(list(self.state.values()), dtype=np.float32), reward, done, False, {}

    def calculate_hp_loss(self):
        """식량 부족으로 인한 HP 감소 계산."""
        base_loss = 10  # 첫 날 HP 감소량
        total_loss = base_loss * (1 + 0.5 * (self.food_depletion_days - 1))  # 가중 HP 감소
        return total_loss

    def handle_exploration_success(self):
        food_gain = 1 + int(self.populationRate * 0.4)  # 인구 밀도에 따른 보상 증가
        self.food += food_gain
        self.food_acquired += food_gain
        print(Fore.GREEN + f"탐색 성공! 음식 {food_gain} 획득. 현재 채력 : {self.state['hp']}")

    def handle_exploration_failure(self):
        self.state["hp"] -= max(5, 15 - self.state["defense"])
        print(Fore.RED + f"탐색 실패로 HP가 감소했습니다. 현재 채력 : {self.state['hp']}")

    def handle_rest(self):
        self.state["hp"] += 1
        print(Fore.CYAN + f"휴식으로 HP가 1 회복되었습니다. 현재 채력 : {self.state['hp']}")

    def calculate_reward(self):
        """생존 일자에 따른 보상 반환."""
        return self.turns_survived  # 생존한 턴 수가 보상

    def calculate_risk_factor(self):
        """인구 밀도에 따른 위험 요소 계산."""
        return 1 / (1 + math.exp(-0.3 * (self.populationRate - 50)))

    def check_done(self):
        """종료 조건 확인: HP가 0이 되면 종료."""
        if self.state["hp"] <= 0:
            self.end_reason = "HP가 0이 되어 종료되었습니다."
            return True
        return False  # 식량이 0이어도 종료되지 않음

    def render(self):
        print(f"State: {self.state}, Food: {self.food}, Turns Survived: {self.turns_survived}")

    def close(self):
        print(f"에피소드 종료! {self.turns_survived} 턴 생존.")
        print(f"종료 원인: {self.end_reason}")
        print(f"총 획득한 음식: {self.food_acquired}")

if __name__ == "__main__":
    # 예제 이미지 인식 결과
    agent_params = {
        "species": 0,
        "attack": 2.5,
        "defense": 2.0,
        "accuracy": 80,
        "weight": 120
    }

    env = CustomSurvivalEnv(populationRate=11, agent_params=agent_params) #! 인구 밀집도 계산 시 주의할 것

    episodes = 5
    for _ in range(episodes):
        obs, _ = env.reset()
        done = False

        while not done:
            action = env.action_space.sample()  # 무작위 행동 선택
            obs, reward, done, _, _ = env.step(action)
            # env.render()

        env.close()
