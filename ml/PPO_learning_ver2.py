import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.distributions import Categorical
from collections import deque
from modules.custom_env_ver2 import CustomSurvivalEnv

class ActorCritic(nn.Module):
    def __init__(self, state_size, action_size):
        super(ActorCritic, self).__init__()
        # Actor 네트워크
        self.actor = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size),
            nn.Softmax(dim=-1)
        )
        # Critic 네트워크
        self.critic = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, state):
        action_probs = self.actor(state)
        state_value = self.critic(state)
        return action_probs, state_value

class PPOAgent:
    def __init__(self, state_size, action_size, lr=0.001, gamma=0.99, eps_clip=0.2):
        self.model = ActorCritic(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma
        self.eps_clip = eps_clip

    def select_action(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action_probs, _ = self.model(state)
        dist = Categorical(action_probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def compute_returns(self, rewards, dones):
        returns = []
        R = 0
        for reward, done in zip(reversed(rewards), reversed(dones)):
            R = reward + self.gamma * R * (1 - done)
            returns.insert(0, R)
        return torch.tensor(returns, dtype=torch.float32)

    def update(self, states, actions, log_probs, rewards, dones):
        returns = self.compute_returns(rewards, dones)
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions)
        old_log_probs = torch.stack(log_probs)

        action_probs, state_values = self.model(states)
        dist = Categorical(action_probs)
        new_log_probs = dist.log_prob(actions)
        entropy = dist.entropy().mean()

        advantages = returns - state_values.squeeze()

        ratio = torch.exp(new_log_probs - old_log_probs.detach())
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
        actor_loss = -torch.min(surr1, surr2).mean()
        critic_loss = nn.functional.mse_loss(state_values.squeeze(), returns)
        loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def save_model(self, path="ppo_model.pth"):
        torch.save(self.model.state_dict(), path)
        print(f"모델이 {path}에 저장되었습니다.")

    def load_model(self, path="ppo_model.pth"):
        self.model.load_state_dict(torch.load(path))
        print(f"{path}에서 모델을 불러왔습니다.")

def train(env, agent, episodes=500, max_steps=300):
    for episode in range(episodes):
        state, _ = env.reset()
        states, actions, log_probs, rewards, dones = [], [], [], [], []
        total_reward = 0

        for _ in range(max_steps):
            action, log_prob = agent.select_action(state)
            next_state, reward, done, _, _ = env.step(action)

            states.append(state)
            actions.append(action)
            log_probs.append(log_prob)
            rewards.append(reward)
            dones.append(done)

            state = next_state
            total_reward += reward

            if done:
                break

        agent.update(states, actions, log_probs, rewards, dones)
        print(f"에피소드 {episode + 1}, 총 보상: {total_reward}")

    # 학습 종료 후 모델 저장
    agent.save_model()

if __name__ == "__main__":
    env = CustomSurvivalEnv(populationRate=15.5)
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = PPOAgent(state_size, action_size)

    # 기존 모델이 있을 경우 로드
    try:
        agent.load_model()
    except FileNotFoundError:
        print("모델이 존재하지 않습니다. 새로운 학습을 시작합니다.")

    train(env, agent, episodes=100)
