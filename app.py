import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (로컬에서 한글 폰트 설치 필요)
plt.rcParams['font.family'] = 'Malgun Gothic'

# CSV 불러오기
df = pd.read_csv("고용노동부_연도별 최저임금_20240805.csv", encoding="cp949")

# 순번 제거
df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 앱 타이틀
st.title("📊 연도별 최저임금 변화 시각화")

# 데이터프레임 출력
st.subheader("최저임금 데이터")
st.dataframe(df)

# 그래프
st.subheader("최저임금의 연도별 변화")
fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o')
ax.set_xlabel('연도')
ax.set_ylabel('시간당 최저임금 (원)')
ax.set_title('연도별 최저임금 변화')
st.pyplot(fig)

