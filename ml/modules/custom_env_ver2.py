import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
import json

# Windows 콘솔을 위한 colorama 초기화

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50, agent_params=None):
        super(CustomSurvivalEnv, self).__init__()

        # 상태 공간 정의: 체력, 공격력, 방어력, 정확도, 체중, 민첩성
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 10, 10, 100, 200, 10], dtype=np.float32),
            dtype=np.float32
        )

        # 행동 공간 정의: 0 = 탐색, 1 = 휴식
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
        self.food_depletion_days = 0
        self.logs = []
        self.last_action = None
        self.exploration_reward = 0  # 탐험 성공 보상 추적용

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        weight = self.agent_params["weight"]

        # 초기 체력과 최대 체력 설정
        initial_hp = 100 + min(100, weight * 0.3)
        self.max_hp = initial_hp

        self.state = {
            "hp": initial_hp,
            "attack": self.agent_params["attack"],
            "defense": self.agent_params["defense"],
            "accuracy": self.agent_params["accuracy"],
            "weight": weight,
            "agility": max(0, 10 - weight * 0.3)
        }

        self.food = min(10, 10 * (1 + self.populationRate / 100))
        self.rest_turns = 0
        self.turns_survived = 0
        self.food_acquired = 0
        self.end_reason = ""
        self.food_depletion_days = 0
        self.logs = []
        self.last_action = None
        self.exploration_reward = 0

        return np.array(list(self.state.values()), dtype=np.float32), {}

    def step(self, action):
        self.turns_survived += 1
        self.food -= 1
        self.last_action = action

        if action == 0:  # 탐색
            success = np.random.rand() > self.calculate_risk_factor()
            if success:
                self.handle_exploration_success()
                self.exploration_reward = 10  # 탐험 성공 보상
            else:
                self.handle_exploration_failure()
                self.exploration_reward = -5  # 탐험 실패 패널티
            self.log_event(f"탐색 수행: {'성공' if success else '실패'}")

        elif action == 1:  # 휴식
            if self.state["hp"] < self.max_hp:
                self.handle_rest()
            self.rest_turns += 1
            self.log_event("휴식을 선택했습니다.")

            if self.rest_turns > 2 and np.random.rand() < 0.3:
                self.handle_intrusion_event()

        if self.food > 0:
            self.state["hp"] = min(self.state["hp"] + 5, self.max_hp)
            self.log_event(f"식량으로 HP가 5 회복되었습니다. 현재 체력: {self.state['hp']}")

        if self.food <= 0:
            self.food_depletion_days += 1
            hp_loss = self.calculate_hp_loss()
            self.state["hp"] -= hp_loss
            self.log_event(f"식량 부족! HP가 {hp_loss} 감소했습니다.")

        reward = self.calculate_reward()
        done = self.check_done()

        return np.array(list(self.state.values()), dtype=np.float32), reward, done, False, {}

    def log_event(self, message):
        day = f"day{self.turns_survived}"
        for log in self.logs:
            if day in log:
                log[day].append(message)
                return
        self.logs.append({day: [message]})

    def calculate_hp_loss(self):
        base_loss = 10
        total_loss = base_loss * (1 + 0.5 * (self.food_depletion_days - 1))
        return total_loss

    def handle_exploration_success(self):
        food_gain = 1 + int(self.populationRate * 0.1)
        self.food += food_gain
        self.food_acquired += food_gain
        self.log_event(f"탐색 성공! 음식 {food_gain} 획득. 현재 체력: {self.state['hp']}")

    def handle_exploration_failure(self):
        self.food = max(0, self.food - 1)
        self.state["hp"] -= max(10, 20 - self.state["defense"])
        self.log_event(f"탐색 실패! 위험 요소와 전투를 진행해 HP가 감소했습니다. 현재 체력: {self.state['hp']}")

    def handle_rest(self):
        self.state["hp"] += 1
        self.log_event(f"휴식으로 HP가 1 회복되었습니다. 현재 체력: {self.state['hp']}")

    def handle_intrusion_event(self):
        self.food = max(0, self.food // 2)
        damage = max(5, 15 - (self.state["defense"] / 2))
        self.state["hp"] -= damage
        self.log_event(f"위험 요소가 침입했습니다! 식량이 절반으로 줄어듭니다. 남은 식량: {self.food}. 현재 체력: {self.state['hp']}")

    def calculate_reward(self):
        reward = 1  # 기본 생존 보상
        reward += self.exploration_reward  # 탐험 결과 반영
        self.exploration_reward = 0  # 리셋
        return reward

    def calculate_risk_factor(self):
        return 1 / (1 + math.exp(-0.6 * (self.populationRate - 50)))

    def check_done(self):
        if self.state["hp"] <= 0:
            self.determine_end_reason()
            self.log_event(self.end_reason)
            return True
        return False

    def determine_end_reason(self):
        if self.food <= 0:
            self.end_reason = "아사했습니다."
        elif self.last_action == 0:
            self.end_reason = "위험 요소로 인해 사망했습니다."
        else:
            self.end_reason = "HP가 0이 되어 종료되었습니다."

    def render(self):
        print(json.dumps(self.logs, indent=2, ensure_ascii=False))

    def close(self):
        print("에피소드 로그:")
        print(json.dumps(self.logs, indent=2, ensure_ascii=False))
        print(f"에피소드 종료! {self.turns_survived} 턴 생존.")
        print(f"종료 원인: {self.end_reason}")
        print(f"총 획득한 음식: {self.food_acquired}")
        
# if __name__ == "__main__":
#     agent_params = {
#         "species": 0,
#         "attack": 2.5,
#         "defense": 2.0,
#         "accuracy": 80,
#         "weight": 120
#     }

#     env = CustomSurvivalEnv(populationRate=15.5, agent_params=agent_params)

#     episodes = 1
#     for _ in range(episodes):
#         obs, _ = env.reset()
#         done = False

#         while not done:
#             action = env.action_space.sample()
#             obs, reward, done, _, _ = env.step(action)

#         env.close()
