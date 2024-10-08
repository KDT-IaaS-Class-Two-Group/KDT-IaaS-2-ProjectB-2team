import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
        super(CustomSurvivalEnv, self).__init__()

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0]), 
            high=np.array([100, 10, 10, 100, 200, 10]), 
            dtype=np.float32
        )
        
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
        zombie_encounter_chance = self.calculate_zombie_encounter_chance()

        if action == 0:  
            if np.random.rand() > zombie_encounter_chance:
                success = True
                self.food += 1

        elif action == 1:  
            self.state["hp"] = min(100, self.state["hp"] + 10)
            if np.random.rand() < 0.05:
                if np.random.rand() < 0.5:
                    success = False

        reward = self.calculate_reward(action, success)

        done = self.state["hp"] <= 0 or self.food <= 0
        truncated = False

        new_state = np.array(list(self.state.values()), dtype=np.float32)
        
        if done and self.food <= 0:
            reward -= 10

        return new_state, reward, done, truncated, {}

    def calculate_zombie_encounter_chance(self):
        base_chance = self.risk_factor
        weight_penalty = max(0, (self.state["weight"] - 70) // 10) * 0.05
        return base_chance + weight_penalty

    def calculate_reward(self, action, success):
        reward = -1

        if action == 0 and success: 
            reward += (self.food * 10)
        
        return reward

    def render(self):
        print(f"State: {self.state}, Food: {self.food}, Risk Factor: {self.risk_factor}")

    def close(self):
        pass