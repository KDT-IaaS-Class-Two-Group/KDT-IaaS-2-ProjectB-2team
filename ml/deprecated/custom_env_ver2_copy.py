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

        # 초기 체력과 최대 체력 설정
        initial_hp = 100 + min(100, weight * 0.3)
        self.max_hp = initial_hp  # 최대 체력을 인스턴스 변수에 저장

        self.state = {
            "hp": initial_hp,  # 초기 체력
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
        self.turns_survived += 1  # 턴 증가
        self.food -= 1  # 식량 감소
        self.last_action = action  # 액션 기록

        # 보상 초기화
        reward = 0

        # 탐색 행동
        if action == 0:  # 탐색
            success = np.random.rand() > self.calculate_risk_factor()
            if success:
                self.handle_exploration_success()
                reward += 5  # 탐색 성공 보상
            else:
                self.handle_exploration_failure()
                reward -= 5  # 탐색 실패 페널티
            self.log_event(f"탐색 수행: {'성공' if success else '실패'}")

        # 휴식 행동
        elif action == 1:  # 휴식
            if self.state["hp"] < 100:
                self.handle_rest()
                reward += 1  # 휴식 보상

            self.rest_turns += 1
            self.log_event("휴식을 선택했습니다.")

            # 휴식 중 침입 이벤트 발생 가능성
            if self.rest_turns > 2 and np.random.rand() < 0.3:
                self.handle_intrusion_event()
                reward -= 10  # 침입 이벤트 페널티

        # 식량 보유에 따른 HP 회복 및 감소 처리
        if self.food > 0:
            self.state["hp"] = min(self.state["hp"] + 5, 100)
            self.log_event(f"식량으로 HP가 5 회복되었습니다. 현재 체력: {self.state['hp']}")
            reward += 2  # 식량으로 인한 보상
        else:
            self.food_depletion_days += 1
            hp_loss = self.calculate_hp_loss()
            self.state["hp"] -= hp_loss
            self.log_event(f"식량 부족! HP가 {hp_loss} 감소했습니다.")
            reward -= hp_loss  # 식량 부족 페널티

        # 종료 조건 체크
        done = self.check_done()

        # 현재 상태 반환
        return np.array(list(self.state.values()), dtype=np.float32), reward, done, False, {}



    def log_event(self, message):
        """현재 턴의 이벤트를 로그에 저장합니다."""
        day = f"day{self.turns_survived}"

        # 이미 해당 날의 로그가 있다면 이벤트를 리스트에 추가
        for log in self.logs:
            if day in log:
                log[day].append(message)
                return

        # 해당 날의 로그가 없으면 새 리스트를 생성하여 추가
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
            f"위험 요소가 침입했습니다! 식량이 절반으로 줄어듭니다. 남은 식량: {self.food}. 현재 체력: {self.state['hp']}"
        )

    def calculate_reward(self):
        """보상을 계산하고 HP 회복 시 최대 체력을 초과하지 않도록 관리."""
        if self.food > 0:
            # 현재 체력에 5를 더하되, 최대 체력을 넘지 않도록 제한
            self.state["hp"] = min(self.max_hp, self.state["hp"] + 5)
            self.log_event(f"식량이 있어 HP가 5 증가했습니다. 현재 체력: {self.state['hp']}")

        return self.turns_survived

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

if __name__ == "__main__":
    agent_params = {
        "species": 0,
        "attack": 2.5,
        "defense": 2.0,
        "accuracy": 80,
        "weight": 120
    }

    env = CustomSurvivalEnv(populationRate=15.5, agent_params=agent_params)

    episodes = 1
    for _ in range(episodes):
        obs, _ = env.reset()
        done = False

        while not done:
            action = env.action_space.sample()
            obs, reward, done, _, _ = env.step(action)

        env.close()
