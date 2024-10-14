import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
from colorama import Fore, Style, init
import json

# Windows 콘솔을 위한 colorama 초기화
init(autoreset=True)

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50, agent_params=None):
        super(CustomSurvivalEnv, self).__init__()

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 10, 10, 100, 200, 10], dtype=np.float32),
            dtype=np.float32
        )

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

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        weight = self.agent_params["weight"]

        self.state = {
            "hp": 100+min(100, weight * 0.3),
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

        return np.array(list(self.state.values()), dtype=np.float32), {}

    def step(self, action):
        self.turns_survived += 1
        self.food -= 1
        self.last_action = action

        if self.food <= 0:
            self.food_depletion_days += 1
            hp_loss = self.calculate_hp_loss()
            self.state["hp"] -= hp_loss
            self.log_event(f"식량 부족! HP가 {hp_loss} 감소했습니다.")

        success = False

        if action == 0:
            success = np.random.rand() > self.calculate_risk_factor()
            if success:
                self.handle_exploration_success()
            else:
                self.handle_exploration_failure()

        elif action == 1:
            if self.state["hp"] < 100:
                self.handle_rest()

            self.rest_turns += 1
            if self.rest_turns > 2 and np.random.rand() < 0.3:
                self.handle_intrusion_event()

        reward = self.calculate_reward()
        done = self.check_done()

        return np.array(list(self.state.values()), dtype=np.float32), reward, done, False, {}

    def log_event(self, message):
        day = f"day{self.turns_survived}"
        self.logs.append({day: message})

    def calculate_hp_loss(self):
        base_loss = 10
        total_loss = base_loss * (1 + 0.5 * (self.food_depletion_days - 1))
        return total_loss

    def handle_exploration_success(self):
        food_gain = 1 + int(self.populationRate * 0.4)
        self.food += food_gain
        self.food_acquired += food_gain
        self.log_event(f"탐색 성공! 음식 {food_gain} 획득. 현재 체력: {self.state['hp']}")

    def handle_exploration_failure(self):
        self.state["hp"] -= max(5, 15 - self.state["defense"])
        self.log_event(f"탐색 실패! 위험 요소와 전투를 진행해 HP가 감소했습니다. 현재 체력: {self.state['hp']}")

    def handle_rest(self):
        self.state["hp"] += 1
        self.log_event(f"휴식으로 HP가 1 회복되었습니다. 현재 체력: {self.state['hp']}")

    def handle_intrusion_event(self):
        """위험 요소 침입 처리: 식량 절반 감소 및 방어력 절반만 적용하여 HP 감소."""
        self.food = max(0, self.food // 2)
        damage = max(5, 15 - (self.state["defense"] / 2))
        self.state["hp"] -= damage

        self.log_event(
            f"위험 요소가 침입했습니다! 식량이 절반으로 줄어듭니다. 남은 식량: {self.food}. "
            f"HP가 {damage} 감소했습니다. 현재 체력: {self.state['hp']}"
        )

    def calculate_reward(self):
        if self.food > 0:
            self.state["hp"] = min(100, self.state["hp"] + 5)
            self.log_event(f"식량이 있어 HP가 5 증가했습니다. 현재 체력: {self.state['hp']}")
        return self.turns_survived

    def calculate_risk_factor(self):
        return 1 / (1 + math.exp(-0.3 * (self.populationRate - 50)))

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
        print(f"에피소드 종료! {self.turns_survived} 턴 생존.")
        print(f"종료 원인: {self.end_reason}")
        print(f"총 획득한 음식: {self.food_acquired}")
        print("에피소드 로그:")
        print(json.dumps(self.logs, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    agent_params = {
        "species": 0,
        "attack": 2.5,
        "defense": 2.0,
        "accuracy": 80,
        "weight": 120
    }

    env = CustomSurvivalEnv(populationRate=1.4, agent_params=agent_params)

    episodes = 1
    for _ in range(episodes):
        obs, _ = env.reset()
        done = False

        while not done:
            action = env.action_space.sample()
            obs, reward, done, _, _ = env.step(action)

        env.close()
