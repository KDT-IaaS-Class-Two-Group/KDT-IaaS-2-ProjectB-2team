# Python 3.8 이미지 기반
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /backend

# 종속성 파일 복사
COPY requirements.txt .

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 컨테이너 시작 시 실행될 명령어
CMD ["python", "main.py"]
