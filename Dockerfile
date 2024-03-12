FROM python:3.11

# OpenJDK 설치 (예시로 OpenJDK 17을 설치)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk fonts-nanum && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# JAVA_HOME 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

# 작업 디렉토리 설정
WORKDIR /app

ARG BRANCH_NAME=team_analytics
ARG DIR_NAME=healthcare_team

# Clone the Git repository. Here we dynamically specify the repository name using the variable defined earlier.
RUN git clone https://github.com/entangelk/marketing_stock ${DIR_NAME}

# Changes the working directory to /app/${REPO_NAME}. This uses the variable to dynamically set the directory path.
WORKDIR /app/${DIR_NAME}


# requirements.txt를 작업 디렉토리로 복사합니다.
COPY requirements.txt .

# 필요한 패키지를 설치합니다.
RUN pip install -r requirements.txt

# RUN pip install --no-cache-dir -r ./requirements.txt
# RUN pip install -r ./requirements.txt

# RUN rm -rf .git

RUN apt -y install wget

RUN apt -y install unzip

RUN apt -y install curl

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt -y install ./google-chrome-stable_current_amd64.deb

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin