import gym
from gym import spaces
import numpy as np
import math
from colorama import Fore, Style, init

# Windows 콘솔을 위한 colorama 초기화
init(autoreset=True)

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
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
        self.medicine_prob = 0  # 의약품 발견 확률
        self.rest_turns = 0  # 휴식 시 턴 수를 기록하는 변수
        self.stat_increases = {"attack": 0, "defense": 0, "accuracy": 0, "agility": 0}
        self.food_acquired = 0  # 획득한 음식량
        self.medicine_acquired = 0  # 획득한 의약품량
        self.turns_survived = 0  # 생존한 턴 수
        self.end_reason = ""  # 종료 원인
        self.base_prob_multiplier = [1, 2, 3]  # 낮은 배수 확률
        self.high_prob_multiplier = [10]  # 높은 배수 (희박한 확률로 발생)
        self.reset()

    def reset(self):
        self.state = {
            "hp": np.random.randint(50, 101),  # 초기 체력: 50~100 사이의 무작위 값
            "attack": np.random.uniform(1.0, 3.0),  # 초기 공격력
            "defense": np.random.uniform(1.0, 3.0),  # 초기 방어력
            "accuracy": np.random.randint(50, 101),  # 초기 정확도
            "weight": np.random.uniform(50, 150),  # 초기 체중
            "agility": np.random.uniform(0, 10)   # 초기 민첩성
        }

        self.food = 100 * (1 + self.populationRate / 100)
        self.medicine_prob = self.populationRate / 150  # 의약품 발견 확률 (인구 밀도에 비례)
        self.rest_turns = 0
        self.stat_increases = {"attack": 0, "defense": 0, "accuracy": 0, "agility": 0}
        self.food_acquired = 0
        self.medicine_acquired = 0
        self.turns_survived = 0
        self.end_reason = ""
        self.risk_factor = self.calculate_risk_factor(self.populationRate)
        return np.array(list(self.state.values()), dtype=np.float32)

    def calculate_risk_factor(self, populationRate):
        return 1 / (1 + math.exp(-0.2 * (populationRate - 50)))  # 위험 확률 증가

    def step(self, action):
        success = False
        self.turns_survived += 1

        # HP가 낮고 음식이 있으면 휴식을 더 선호
        if self.state["hp"] < 50 and self.food > 0 and np.random.rand() < 0.95:  # 95% 확률로 휴식을 선택
            action = 1  # 휴식을 선택하도록 강제

        if action == 0:  # 탐색
            # 낮은 확률로 매우 강력한 적을 만남
            if np.random.rand() < 0.05:  # 5% 확률로 매우 강력한 적 조우
                print(Fore.RED + "매우 강력한 적을 만났습니다!")
                success = self.fight_strong_enemy()
            else:
                success = np.random.rand() > self.risk_factor  # 위험 요소와의 조우 여부 결정
                if success:
                    self.handle_exploration_success()
                else:
                    self.handle_exploration_failure()

        elif action == 1:  # 휴식
            if self.state["hp"] < 100 and self.food > 0:  # HP가 100 이하일 때만 휴식
                self.handle_rest()

        reward = self.calculate_reward(action, success)
        done = self.check_done()

        # 음식 소모량 증가: 체중에 비례하여 음식 소모량 증가
        food_consumption = max(1, self.state["weight"] / 50)  # 체중에 따라 소모량 증가
        self.food -= food_consumption

        return np.array(list(self.state.values()), dtype=np.float32), reward, done, {}

    def fight_strong_enemy(self):
        """ 매우 강력한 적과 싸우는 메서드, 성공 시 큰 보상, 실패 시 큰 페널티 """
        if np.random.rand() < (self.state["attack"] + self.state["defense"]) / 20:  # 능력에 따라 승리 확률 결정
            print(Fore.GREEN + "강력한 적을 물리쳤습니다! 능력치가 소폭 증가합니다.")
            self.increase_random_stat()
            return True
        else:
            damage = max(5, 25 - self.state["defense"])  # 강력한 적에게서 받는 피해량
            self.state["hp"] -= damage
            print(Fore.RED + f"강력한 적에게 패배했습니다. HP가 {damage}만큼 감소했습니다.")
            return False

    def handle_exploration_success(self):
        if np.random.rand() < 0.85:  # 85% 확률로 음식 발견
            self.food += 10
            self.food_acquired += 10
            print(Fore.GREEN + "탐색 성공! 음식 발견.")
        else:  # 15% 확률로 의약품 발견
            self.medicine_acquired += 1
            self.state["hp"] = min(100, self.state["hp"] + 5)
            print(Fore.GREEN + "탐색 성공! 의약품 발견, HP +5.")

    def handle_exploration_failure(self):
        if np.random.rand() < 0.05:  # 탐색 실패 시 매우 적은 확률로 능력치 감소
            self.decrease_random_stat()  # 능력치 감소 메서드 추가
            print(Fore.YELLOW + "탐색 실패... 능력치가 감소했습니다.")
        else:
            self.state["hp"] -= max(5, 15 - self.state["defense"])  # 방어력에 따라 피해 감소
            print(Fore.RED + "탐색 실패, HP가 감소했습니다.")

    def decrease_random_stat(self):
        stat = np.random.choice(["attack", "defense", "accuracy", "agility"])
        self.state[stat] = max(0, self.state[stat] - 0.1)  # 능력치 감소량 소폭 증가
        self.stat_increases[stat] -= 0.1
        print(Fore.CYAN + f"{stat} 능력치가 감소했습니다.")

    def handle_rest(self):
        self.state["hp"] += 1  # 기본 HP 회복을 줄임
        self.rest_turns += 1

        if np.random.rand() < 0.1:  # 휴식 시 10% 확률로 스탯 소폭 증가
            self.increase_random_stat()

    def increase_random_stat(self):
        stat = np.random.choice(["attack", "defense", "accuracy", "agility"])
        self.state[stat] += 0.1  # 능력치 증가량 소폭 감소
        self.stat_increases[stat] += 0.1
        print(Fore.CYAN + f"{stat} 능력치가 증가했습니다.")

    def calculate_reward(self, action, success):
        reward = 1  # 기본 보상
        if action == 0 and success:
            reward += 10
        elif action == 0 and not success:
            reward -= 10
        return reward

    def check_done(self):
        done = False
        if self.state["hp"] <= 0:
            self.end_reason = "HP가 0이 되어 종료되었습니다."
            done = True
        elif self.food <= 0:
            self.end_reason = "음식이 부족하여 종료되었습니다."
            done = True
        return done

    def render(self):
        print(f"State: {self.state}, Food: {self.food}, Risk Factor: {self.risk_factor}")

    def close(self):
        print(f"에피소드 종료! {self.turns_survived} 턴 생존.")
        print(f"종료 원인: {self.end_reason}")
        print(f"총 획득한 음식: {self.food_acquired}, 총 획득한 의약품: {self.medicine_acquired}")
        print(f"능력치 증가량: {self.stat_increases}")

if __name__ == "__main__":
    env = CustomSurvivalEnv()  # 환경 초기화
    obs = env.reset()  # 환경 초기화 및 첫 번째 상태 받기

    done = False
    total_reward = 0

    while not done:
        env.render()  # 현재 상태 출력
        action = env.action_space.sample()  # 무작위로 행동 선택
        obs, reward, done, info = env.step(action)  # 행동 후 상태, 보상, 종료 여부 확인
        total_reward += reward  # 보상 누적

    env.close()  # 환경 종료
    print(f"총 보상: {total_reward}")
