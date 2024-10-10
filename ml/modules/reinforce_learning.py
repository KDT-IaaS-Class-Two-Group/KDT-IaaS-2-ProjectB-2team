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
        self.action_space = spaces.Discrete(3)  # 탐색(0), 휴식(1), 거점이동(2)
        
        self.populationRate = populationRate
        self.state = None
        self.food = 5  # 기본 식량 5개
        self.medicine = 0  # 초기 의약품 없음
        self.risk_factor = None
        self.sound_prob = 0.05  # 초기 소음 발생 확률
        self.current_zone = None  # 시작 구역은 랜덤
        self.days_survived = 0  # 생존한 날짜
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.state = {
            "hp": np.random.randint(90, 101),  # 플레이어 체력 50~100
            "attack": np.random.uniform(9.0, 10.0),  # 공격력 1.0~3.0
            "defense": np.random.uniform(2.0, 3.0),  # 방어력 1.0~3.0
            "accuracy": np.random.randint(90, 101),  # 정확도 50~100
            "weight": np.random.uniform(80, 90),  # 무게 50~150
            "agility": np.random.uniform(5, 7)  # 민첩성 0~10
        }

        self.zombie = {  # 좀비 능력치 설정 
            "hp": np.random.randint(30, 32),  
            "attack": np.random.uniform(2.0, 2.3),  
            "defense": np.random.uniform(0.9, 1.0), 
            "accuracy": np.random.randint(50, 60), 
        }
        
        self.food = 5  # 식량은 5개로 초기화
        self.medicine = 0  # 의약품 없음
        self.risk_factor = self.calculate_risk_factor(self.populationRate)
        self.sound_prob = 0.05  # 소음 확률 초기화
        self.current_zone = np.random.randint(1, 5)  # 시작 구역 랜덤으로 설정
        self.days_survived = 0  # 생존한 날짜 초기화
        
        return np.array(list(self.state.values()), dtype=np.float32), {}

    def calculate_risk_factor(self, populationRate):
        return 1 / (1 + math.exp(-0.1 * (populationRate - 50)))

    def calculate_zone_effects(self, zone):
        """거점 구역에 따른 효과 적용"""
        if zone == 1:  # 대도시
            food_prob_modifier = 0.2  # 식량 확률 +20%
            zombie_prob_modifier = 0.1  # 좀비 만날 확률 +10%
        elif zone == 2:  # 도시
            food_prob_modifier = 0.1  # 식량 확률 +10%
            zombie_prob_modifier = 0.05  # 좀비 만날 확률 +5%
        elif zone == 3:  # 중소도시
            food_prob_modifier = 0.0  # 식량 확률 0%
            zombie_prob_modifier = 0.0  # 좀비 만날 확률 0%
        else:  # 시골
            food_prob_modifier = -0.05  # 식량 확률 -5%
            zombie_prob_modifier = -0.1  # 좀비 만날 확률 -10%
        return food_prob_modifier, zombie_prob_modifier

    def step(self, action):
        success = False
        food_prob_modifier, zombie_prob_modifier = self.calculate_zone_effects(self.current_zone)
        
        if action == 0:  # 탐색
            success = np.random.rand() > (0.3 + zombie_prob_modifier)
            food_found = np.random.rand() < (0.7 + food_prob_modifier)  # 식량 획득 확률
            medicine_found = np.random.rand() < 0.1  # 의약품 10% 확률로 획득
            if success:
                if food_found:
                    self.food += 1
                    print("탐색 중 식량을 찾았습니다!")
                if medicine_found:
                    self.medicine += 1
                    print("탐색 중 의약품을 찾았습니다!")
                
                # 체중에 따른 좀비 조우 확률 계산
                weight_effect = max(0, (self.state['weight'] - 70) // 10) * 0.02
                encounter_prob = self.risk_factor + weight_effect + zombie_prob_modifier
                print(f"탐색 중 좀비와 마주칠 확률: {encounter_prob:.2f}")
                if np.random.rand() < encounter_prob:
                    print("좀비가 전투 중 마주쳤습니다!")
                    self.fight_zombie()
            else:
                print("탐색 실패! 좀비를 만났습니다.")
                self.fight_zombie()

        elif action == 1:  # 휴식
            self.state["hp"] = min(100, self.state["hp"] + 10)
            print(f"휴식 중 체력이 회복되었습니다. 현재 체력: {self.state['hp']}")
            # 소음이 발생할 확률 계산
            self.sound_prob = min(1.0, self.sound_prob + 0.05)
            if np.random.rand() < self.sound_prob:
                print(f"휴식 중 소음이 발생하여 좀비가 찾아왔습니다! 소음 확률: {self.sound_prob}")
                self.fight_zombie()

        elif action == 2:  # 거점 이동
            self.sound_prob = 0.05  # 소음 확률 리셋
            self.food -= 1  # 식량 감소
            self.current_zone = np.random.randint(1, 5)  # 거점을 무작위로 이동
            print(f"거점 이동 완료. 새로운 구역: {self.current_zone}")
            self.medicine += 1  # 의약품 무조건 획득
            print("이동 중 의약품을 획득했습니다!")
            
            # 50% 확률로 좀비와 조우
            if np.random.rand() < 0.5:
                print("거점 이동 중 좀비를 만났습니다!")
                self.fight_zombie()

        # 날짜 증가
        self.days_survived += 1
        
        # 식량이 없으면 체력 감소
        if self.food <= 0:
            self.state["hp"] = max(0, self.state["hp"] - 10)

        reward = self.calculate_reward(action, success)
        done = self.state["hp"] <= 0 or self.food <= 0
        truncated = False
        
        new_state = np.array(list(self.state.values()), dtype=np.float32)
        return new_state, reward, done, truncated, {}

    def fight_zombie(self):
        """좀비와 전투를 처리하는 메서드"""
        zombie_attacks = 0  # 좀비가 공격한 횟수 초기화

        for turn in range(10):  # 10회 공격 주고받기
            # 플레이어의 공격
            if np.random.rand() < (self.state["accuracy"] / 100):  # 공격 성공 확률
                damage = max(0, self.state["attack"] - self.zombie["defense"])  # 최종 데미지 계산
                self.zombie["hp"] -= damage  # 좀비 HP 감소
                print(f"플레이어가 좀비를 공격! 좀비에게 {damage} 피해를 입혔습니다.")
            else:
                print("플레이어의 공격이 빗나갔습니다.")

            # 좀비가 살아있을 경우, 좀비의 공격
            if self.zombie["hp"] > 0:
                if np.random.rand() < (self.zombie["accuracy"] / 100):  # 공격 성공 확률
                    damage = max(0, self.zombie["attack"] - self.state["defense"])  # 최종 데미지 계산
                    self.state["hp"] -= damage  # 플레이어 HP 감소
                    zombie_attacks += 1  # 좀비 공격 횟수 증가
                    print(f"좀비가 플레이어를 공격! 플레이어에게 {damage} 피해를 입혔습니다.")
                else:
                    print("좀비의 공격이 빗나갔습니다.")

            # 플레이어의 HP가 0 이하인지 확인
            if self.state["hp"] <= 0:
                print("플레이어가 사망했습니다.")
                break  # 플레이어가 죽으면 전투 종료

            # 좀비의 HP가 0 이하인지 확인
            if self.zombie["hp"] <= 0:
                print("좀비를 처치했습니다!")
                break  # 좀비가 죽으면 전투 종료

        # 전투가 끝난 후, 좀비가 살아있다면 플레이어 체력 5 감소
        if self.zombie["hp"] > 0:
            self.state["hp"] -= 5
            print("좀비가 살아남았습니다! 플레이어의 체력이 5 감소합니다.")
            
        # 플레이어의 HP가 좀비 공격 횟수만큼 감소했는지 반영
        if zombie_attacks > 0:
            self.state["hp"] = max(0, self.state["hp"] - zombie_attacks)

        # 최종 HP 확인
        if self.state["hp"] <= 0:
            print("플레이어가 사망했습니다.")


    def calculate_reward(self, action, success):
        reward = 1
        
        if action == 0:  # 탐색
            if success:
                reward += 10 + (self.risk_factor * 10)
            else:
                reward -= 10 + (self.risk_factor * 5)
        elif action == 1:  # 휴식
            reward += 2 if self.state["hp"] < 50 else 1
        elif action == 2:  # 거점 이동
            reward += 10  # 의약품 획득 보상
            
        # 식량 소비
        self.food -= 1
        if self.food <= 0:
            reward -= 10
            self.state["agility"] = max(0, self.state["agility"] - 0.5)
            self.state["hp"] = max(0, self.state["hp"] - 1)
        
        return reward

    def render(self, mode='human'):
        print(f"State: {self.state}, Food: {self.food}, Medicine: {self.medicine}, Risk Factor: {self.risk_factor}, Zone: {self.current_zone}, Sound Probability: {self.sound_prob}, Days Survived: {self.days_survived}")

# 환경 사용 예
env = CustomSurvivalEnv()
obs, info = env.reset()
env.render()

for _ in range(10):
    action = env.action_space.sample()  # 랜덤 행동 선택
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        print("게임 종료!")
        break
