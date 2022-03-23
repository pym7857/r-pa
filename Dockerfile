# Dockerfile

# python 3.8 버전 Image 불러오기
FROM python:3.8
# FROM winamd64/python:3.8 # for windows container

# Container 내부의 작업경로 설정
WORKDIR /app

# python requirments 설치
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

# container 외부로 노출할 port 설정(서버의 port와는 다름!)
EXPOSE 8504

# 소스코드를 /app으로 복사
COPY . /app

# container 시작 시 실행할 command 입력
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py","--server.headless=true", "--global.developmentMode=false"]
