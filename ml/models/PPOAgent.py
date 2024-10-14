import torch
import torch.nn as nn

class PPOAgent:
    def __init__(self, state_dim, action_dim):
        # 네트워크 구조 정의
        self.policy = nn.ModuleDict({
            'fc1': nn.Linear(state_dim, 128),
            'fc2': nn.Linear(128, 128),
            'action_head': nn.Linear(128, action_dim),
            'value_head': nn.Linear(128, 1)
        })

    def forward(self, x):
        x = torch.relu(self.policy['fc1'](x))
        x = torch.relu(self.policy['fc2'](x))
        action_probs = torch.softmax(self.policy['action_head'](x), dim=-1)
        state_value = self.policy['value_head'](x)
        return action_probs, state_value

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        action_probs, _ = self.forward(state)
        action = torch.multinomial(action_probs, 1).item()
        return action, action_probs

    def load_model(self, file_path):
        """모델 로드 함수"""
        state_dict = torch.load(file_path, weights_only=True)
        self.policy.load_state_dict(state_dict)
        self.policy.eval()  # 평가 모드로 전환
        print(f"모델이 로드되었습니다: {file_path}")
