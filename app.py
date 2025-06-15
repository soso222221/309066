import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from sklearn.linear_model import LinearRegression
import numpy as np

# ✅ 한글 폰트 설정
font_path = os.path.join(os.getcwd(), "NanumHumanRegular.ttf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    plt.rcParams['font.family'] = [font_name]
    plt.rcParams['axes.unicode_minus'] = False
    st.success(f"✅ 한글 폰트 적용됨: {font_name}")
else:
    st.warning("⚠️ NanumGothic.ttf 파일이 없습니다. 한글이 깨질 수 있어요.")

# 📌 제목
st.title("📈 연도별 최저임금 변화 및 예측")

# 📊 데이터 불러오기
csv_file = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_file, encoding="cp949")
except:
    df = pd.read_csv(csv_file, encoding="utf-8")

# 🔍 데이터 정리
df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 🧾 데이터 출력
st.subheader("🗂 최저임금 데이터")
st.dataframe(df)

# ✅ 머신러닝: 선형 회귀 예측
X = df[['연도']]
y = df['시간급']
model = LinearRegression()
model.fit(X, y)

# 📅 미래 연도 예측 (2026~2028)
future_years = np.array([[2026], [2027], [2028]])
future_pred = model.predict(future_years)
future_df = pd.DataFrame({
    '연도': future_years.flatten(),
    '예상 시간급': future_pred.astype(int)
})

# 📉 시각화
st.subheader("📉 최저임금 변화 및 예측 그래프")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', label='실제 최저임금')
ax.plot(future_df['연도'], future_df['예상 시간급'], marker='x', linestyle='--', label='예상 최저임금')
ax.set_xlabel("연도", fontproperties=font_prop)
ax.set_ylabel("시간급 (원)", fontproperties=font_prop)
ax.set_title("최저임금의 연도별 변화", fontproperties=font_prop)
ax.grid(True)
ax.legend()
st.pyplot(fig)

# 📄 예측 테이블 출력
st.subheader("🔮 2026~2028년 최저임금 예측")
st.dataframe(future_df)

# 📎 출처
st.markdown("---")
st.markdown("📌 출처: 고용노동부")
