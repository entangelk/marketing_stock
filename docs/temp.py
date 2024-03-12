import pandas as pd

# 크롤링한 데이터
data = [{'Name': 'John', 'Age': 30, 'City': 'New York'},
        {'Name': 'Emma', 'Age': 25, 'City': 'Los Angeles'},
        {'Name': 'Ryan', 'Age': 35, 'City': 'Chicago'}]

# 데이터프레임 생성
df = pd.DataFrame(data)

# CSV 파일로 저장 (헤더를 한 번만 작성)
df.to_csv('data.csv', index=False)
