import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import gymnasium as gym
import numpy as np
import os

from modules.custom_env import CustomSurvivalEnv  # 사용자 정의 환경

torch.autograd.set_detect_anomaly(True)  # 이상 탐지 활성화

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.action_head = nn.Linear(128, action_dim)
        self.value_head = nn.Linear(128, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        action_probs = torch.softmax(self.action_head(x), dim=-1)
        state_value = self.value_head(x)
        return action_probs, state_value

class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, clip_epsilon=0.2):
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        action_probs, _ = self.policy(state)
        dist = Categorical(action_probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action).detach()

    def compute_returns(self, rewards, dones, next_value):
        returns = []
        R = next_value
        for step in reversed(range(len(rewards))):
            R = rewards[step] + self.gamma * R * (1 - dones[step])
            returns.insert(0, R)
        return returns

    def update(self, states, actions, log_probs, rewards, dones, next_state):
        next_state = torch.FloatTensor(next_state).unsqueeze(0)
        _, next_value = self.policy(next_state)
        returns = self.compute_returns(rewards, dones, next_value.item())

        returns = torch.FloatTensor(returns)
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions)
        old_log_probs = torch.stack(log_probs)

        for _ in range(10):
            self.optimizer.zero_grad()

            action_probs, state_values = self.policy(states)
            dist = Categorical(action_probs)
            new_log_probs = dist.log_prob(actions)

            ratios = torch.exp(new_log_probs - old_log_probs)
            advantages = (returns - state_values.squeeze(1)).detach()

            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            loss = -torch.min(surr1, surr2).mean() + 0.5 * (advantages ** 2).mean() - 0.01 * dist.entropy().mean()

            loss.backward()
            self.optimizer.step()

    def save_model(self, file_path):
        """모델 저장"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        torch.save(self.policy.state_dict(), file_path)
        print(f"모델이 저장되었습니다: {file_path}")

    def load_model(self, file_path):
        """모델 로드"""
        self.policy.load_state_dict(torch.load(file_path))
        print(f"모델이 로드되었습니다: {file_path}")

def train(env, agent, num_episodes=1000, max_steps=500, save_path="ppo_model.pth"):
    for episode in range(num_episodes):
        state, _ = env.reset()
        log_probs, rewards, states, actions, dones = [], [], [], [], []

        total_reward, done = 0, False

        for step in range(max_steps):
            action, log_prob = agent.select_action(state)
            next_state, reward, done, _, _ = env.step(action)

            log_probs.append(log_prob)
            rewards.append(reward)
            states.append(state)
            actions.append(action)
            dones.append(done)

            state = next_state
            total_reward += reward

            if done:
                break

        agent.update(states, actions, log_probs, rewards, dones, state)
        print(f"에피소드 {episode + 1}: 총 보상 = {total_reward}")

    # 학습 종료 후 모델 저장
    agent.save_model(save_path)

if __name__ == "__main__":
    env = CustomSurvivalEnv()
    agent = PPOAgent(env.observation_space.shape[0], env.action_space.n)

    # 학습 후 모델 저장
    train(env, agent, save_path="models/ppo_model.pth")

    # 저장된 모델 로드 및 테스트
    # agent.load_model("models/ppo_model.pth")
