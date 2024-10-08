import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
        super(CustomSurvivalEnv, self).__init__()
        
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0]), 
                                            high=np.array([100, 10, 10, 100, 200, 10]), 
                                            dtype=np.float32)
        self.action_space = spaces.Discrete(2)
        
        self.populationRate = populationRate
        self.state = None
        self.food = None
        self.risk_factor = None
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.state = {
            "hp": np.random.randint(50, 101),
            "attack": np.random.uniform(1.0, 3.0),
            "defense": np.random.uniform(1.0, 3.0),
            "accuracy": np.random.randint(50, 101),
            "weight": np.random.uniform(50, 150),
            "agility": np.random.uniform(0, 10)
        }
        
        self.food = 100 * (1 + self.populationRate / 100)
        self.risk_factor = self.calculate_risk_factor(self.populationRate)
        
        return np.array(list(self.state.values()), dtype=np.float32), {}

    def calculate_risk_factor(self, populationRate):
        return 1 / (1 + math.exp(-0.1 * (populationRate - 50)))

    def step(self, action):
        success = False
        
        if action == 0:  # 탐색
            success = np.random.rand() > self.risk_factor
            if success:
                self.food += 1
                # 체중에 따른 좀비 조우 확률 계산
                weight_effect = max(0, (self.state['weight'] - 70) // 10) * 0.05
                encounter_prob = self.risk_factor + weight_effect
                print(f"탐색 중 좀비와 마주칠 확률: {encounter_prob:.2f}")
                if np.random.rand() < encounter_prob:
                    print("좀비가 전투 중 마주쳤습니다!")
        elif action == 1:  # 휴식
            self.state["hp"] = min(100, self.state["hp"] + 10)
            if np.random.rand() < 0.05:  # 5% 확률로 소음 발생
                if np.random.rand() < 0.5:  # 50% 확률로 좀비 출현
                    print("좀비가 휴식 시 소음 때문에 다가왔습니다!")

        reward = self.calculate_reward(action, success)
        done = self.state["hp"] <= 0 or self.food <= 0
        truncated = False
        
        new_state = np.array(list(self.state.values()), dtype=np.float32)
        return new_state, reward, done, truncated, {}

    def calculate_reward(self, action, success):
        reward = 1
        
        if action == 0:  # 탐색
            if success:
                reward += 10 + (self.risk_factor * 10)
            else:
                reward -= 10 + (self.risk_factor * 5)
        elif action == 1:  # 휴식
            reward += 2 if self.state["hp"] < 50 else 1
        
        self.food -= 1
        if self.food <= 0:
            reward -= 10
            self.state["agility"] = max(0, self.state["agility"] - 0.5)
            self.state["hp"] = max(0, self.state["hp"] - 1)
        
        return reward

    def render(self, mode='human'):
        print(f"State: {self.state}, Food: {self.food}, Risk Factor: {self.risk_factor}")

    def close(self):
        pass