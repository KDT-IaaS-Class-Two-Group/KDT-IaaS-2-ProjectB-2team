population_data = {
    "서울": 15533,
    "부산": 4258,
    "대구": 2666,
    "인천": 2820,
    "광주": 2921,
    "대전": 2731,
    "울산": 1041,
    "세종": 833,
    "경기": 1351,
    "강원": 91,
    "충북": 220,
    "충남": 267,
    "전북": 219,
    "전남": 143,
    "경북": 137,
    "경남": 310,
    "제주": 366
}

def preprocess_population_density(city):
    # 선택된 도시의 인구 밀도 값
    density = population_data.get(city, 0)

    # 밀도를 1000으로 나눔
    adjusted_density = density / 1000

    # 1000으로 나눈 값이 0.1보다 작으면 100으로 나눔
    if adjusted_density < 0.1:
        adjusted_density = density / 100

    return adjusted_density

# 예시: 프론트에서 '서울'이라는 도시 입력을 받아 처리
city_name = "서울"
population_rate = preprocess_population_density(city_name)
print(f"{city_name}의 전처리된 인구 밀도: {population_rate}")