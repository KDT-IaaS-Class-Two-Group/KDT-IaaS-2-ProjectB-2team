import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

# Windows 콘솔을 위한 colorama 초기화
init(autoreset=True)

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
        super(CustomSurvivalEnv, self).__init__()

        # 상태 공간 정의: HP, 공격력, 방어력, 정확도, 체중, 민첩성
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 10, 10, 100, 200, 10], dtype=np.float32),
            dtype=np.float32
        )

        # 행동 공간 정의: 탐색(0), 휴식(1)
        self.action_space = spaces.Discrete(2)

        self.populationRate = populationRate  # 인구 밀도 설정
        self.state = None
        self.food = None
        self.risk_factor = None
        self.medicine_prob = 0  # 의약품 발견 확률
        self.rest_turns = 0  # 휴식 시 턴 수 기록
        self.stat_increases = {"attack": 0, "defense": 0, "accuracy": 0, "agility": 0}
        self.food_acquired = 0  # 획득한 음식량
        self.medicine_acquired = 0  # 획득한 의약품량
        self.turns_survived = 0  # 생존한 턴 수
        self.end_reason = ""  # 종료 원인
        self.base_prob_multiplier = [1, 2, 3]  # 낮은 배수 확률
        self.high_prob_multiplier = [10]  # 높은 배수 (희박한 확률로 발생)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # `gymnasium`의 reset 호출 방식 수정
        self.state = {
            "hp": np.random.randint(50, 101),  # 초기 체력: 50~100 사이의 무작위 값
            "attack": np.random.uniform(1.0, 3.0),
            "defense": np.random.uniform(1.0, 3.0),
            "accuracy": np.random.randint(50, 101),
            "weight": np.random.uniform(50, 150),
            "agility": np.random.uniform(0, 10)
        }

        self.food = 100 * (1 + self.populationRate / 100)
        self.medicine_prob = self.populationRate / 150
        self.rest_turns = 0
        self.stat_increases = {"attack": 0, "defense": 0, "accuracy": 0, "agility": 0}
        self.food_acquired = 0
        self.medicine_acquired = 0
        self.turns_survived = 0
        self.end_reason = ""
        self.risk_factor = self.calculate_risk_factor(self.populationRate)

        return np.array(list(self.state.values()), dtype=np.float32), {}  # 새로운 gymnasium 형식 반환

    def calculate_risk_factor(self, populationRate):
        return 1 / (1 + math.exp(-0.2 * (populationRate - 50)))

    def step(self, action):
        success = False
        self.turns_survived += 1

        if self.state["hp"] < 50 and self.food > 0 and np.random.rand() < 0.95:
            action = 1

        if action == 0:
            if np.random.rand() < 0.05:
                print(Fore.RED + "매우 강력한 적을 만났습니다!")
                success = self.fight_strong_enemy()
            else:
                success = np.random.rand() > self.risk_factor
                if success:
                    self.handle_exploration_success()
                else:
                    self.handle_exploration_failure()

        elif action == 1:
            if self.state["hp"] < 100 and self.food > 0:
                self.handle_rest()

        reward = self.calculate_reward(action, success)
        done = self.check_done()

        food_consumption = max(1, self.state["weight"] / 50)
        self.food -= food_consumption

        return np.array(list(self.state.values()), dtype=np.float32), reward, done, False, {}

    def fight_strong_enemy(self):
        if np.random.rand() < (self.state["attack"] + self.state["defense"]) / 20:
            print(Fore.GREEN + "강력한 적을 물리쳤습니다! 능력치가 증가합니다.")
            self.increase_random_stat()
            return True
        else:
            damage = max(5, 25 - self.state["defense"])
            self.state["hp"] -= damage
            print(Fore.RED + f"강력한 적에게 패배했습니다. HP가 {damage}만큼 감소했습니다.")
            return False

    def handle_exploration_success(self):
        if np.random.rand() < 0.85:
            self.food += 10
            self.food_acquired += 10
            print(Fore.GREEN + "탐색 성공! 음식 발견.")
        else:
            self.medicine_acquired += 1
            self.state["hp"] = min(100, self.state["hp"] + 5)
            print(Fore.GREEN + "탐색 성공! 의약품 발견, HP +5.")

    def handle_exploration_failure(self):
        if np.random.rand() < 0.05:
            self.decrease_random_stat()
            print(Fore.YELLOW + "탐색 실패... 능력치가 감소했습니다.")
        else:
            self.state["hp"] -= max(5, 15 - self.state["defense"])
            print(Fore.RED + "탐색 실패, HP가 감소했습니다.")

    def decrease_random_stat(self):
        stat = np.random.choice(["attack", "defense", "accuracy", "agility"])
        self.state[stat] = max(0, self.state[stat] - 0.1)
        self.stat_increases[stat] -= 0.1
        print(Fore.CYAN + f"{stat} 능력치가 감소했습니다.")

    def handle_rest(self):
        self.state["hp"] += 1
        self.rest_turns += 1

        if np.random.rand() < 0.1:
            self.increase_random_stat()

    def increase_random_stat(self):
        stat = np.random.choice(["attack", "defense", "accuracy", "agility"])
        self.state[stat] += 0.1
        self.stat_increases[stat] += 0.1
        print(Fore.CYAN + f"{stat} 능력치가 증가했습니다.")

    def calculate_reward(self, action, success):
        reward = 1
        if action == 0 and success:
            reward += 10
        elif action == 0 and not success:
            reward -= 10
        return reward

    def check_done(self):
        if self.state["hp"] <= 0:
            self.end_reason = "HP가 0이 되어 종료되었습니다."
            return True
        elif self.food <= 0:
            self.end_reason = "음식이 부족하여 종료되었습니다."
            return True
        return False

    def render(self):
        print(f"State: {self.state}, Food: {self.food}, Risk Factor: {self.risk_factor}")

    def close(self):
        print(f"에피소드 종료! {self.turns_survived} 턴 생존.")
        print(f"종료 원인: {self.end_reason}")
        print(f"총 획득한 음식: {self.food_acquired}, 총 획득한 의약품: {self.medicine_acquired}")
        print(f"능력치 증가량: {self.stat_increases}")

if __name__ == "__main__":
    env = CustomSurvivalEnv()

    episodes = 500
    total_rewards = []

    for _ in range(episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0

        while not done:
            action = env.action_space.sample()
            obs, reward, done, _, _ = env.step(action)
            total_reward += reward

        env.close()
        total_rewards.append(total_reward)

    plt.plot(total_rewards, marker='o')
    plt.title("Total Rewards Over Episodes")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.grid()
    plt.show()
