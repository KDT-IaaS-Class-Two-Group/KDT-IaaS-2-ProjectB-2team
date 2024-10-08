import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math

class CustomSurvivalEnv(gym.Env):
    def __init__(self, populationRate=50):
        super(CustomSurvivalEnv, self).__init__()

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0]), 
            high=np.array([100, 10, 10, 100, 200, 10, 10, 1]), 
            dtype=np.float32
        )
        
        self.action_space = spaces.Discrete(2)

        self.populationRate = populationRate
        self.state = None
        self.food = None
        self.sound_probability = 0.1
        self.zombie_encounter = False
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.state = {
            "hp": np.random.randint(50, 101),
            "attack": np.random.uniform(1.0, 3.0),
            "defense": np.random.uniform(1.0, 3.0),
            "accuracy": np.random.randint(50, 101),
            "weight": np.random.uniform(50, 150),
            "agility": np.random.uniform(0, 10),
            "sound": 0,
            "zombie": 0
        }

        self.food = 3 + int(self.populationRate / 10)  
        return np.array(list(self.state.values()), dtype=np.float32), {}

    def step(self, action):
        success = False
        self.zombie_encounter = False
        self.state["sound"] = 0

        if action == 0:  
            if np.random.rand() < 0.6:
                success = True
                self.food += 1
                if np.random.rand() < 0.05:
                    self.state["hp"] = min(100, self.state["hp"] + 50)
            else:
                if np.random.rand() < 0.3:
                    self.zombie_encounter = True

        elif action == 1:  
            self.state["hp"] = min(100, self.state["hp"] + 10)
            if np.random.rand() < self.sound_probability:
                self.state["sound"] = 1
                if np.random.rand() < (0.5 + (self.sound_probability * 5)): 
                    self.zombie_encounter = True

            if not self.zombie_encounter:
                success = True

        if self.zombie_encounter:
            fight_result = self._fight_zombie()
            if not fight_result:
                self.state["hp"] = max(0, self.state["hp"] - 10)

        reward = self.calculate_reward(action, success)

        done = self.state["hp"] <= 0 or self.food <= 0
        truncated = False

        new_state = np.array(list(self.state.values()), dtype=np.float32)
        
        if done and self.food <= 0:
            reward -= 10

        return new_state, reward, done, truncated, {}

    def _fight_zombie(self):
        player_attack = self.state["attack"]
        player_defense = self.state["defense"]
        player_accuracy = self.state["accuracy"]

        zombie_attack = np.random.uniform(2.0, 5.0)
        zombie_defense = np.random.uniform(1.0, 4.0)

        return player_accuracy * player_attack > zombie_attack * zombie_defense

    def calculate_reward(self, action, success):
        reward = -1

        if action == 0 and success: 
            reward += (self.food * 10)
        
        return reward

    def render(self):
        print(f"State: {self.state}, Food: {self.food}, Zombie Encounter: {self.zombie_encounter}")

    def close(self):
        pass