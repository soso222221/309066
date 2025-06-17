import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# ✅ 한글 폰트 설정
font_path = os.path.join(os.getcwd(), "NanumHumanRegular.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())  # 모든 matplotlib에 한글 globally!
    plt.rcParams['axes.unicode_minus'] = False
    st.success("✅ NanumHumanRegular.ttf 폰트 적용 완료")
else:
    font_prop = None
    st.warning("⚠️ NanumHumanRegular.ttf 파일이 없습니다.")

# ✅ 제목
st.markdown("## 최저임금의 연도별 변화")

# 📊 데이터 불러오기
csv_file = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_file, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding="utf-8")

df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 🧾 데이터 표시
st.markdown("### 최저임금 원본 데이터 🗂")
st.dataframe(df)

# ✅ 머신러닝 예측 (선형 회귀)
X = df[['연도']]
y = df['시간급']
model = LinearRegression()
model.fit(X, y)

future_years = np.array([[2026], [2027], [2028]])
future_pred = model.predict(future_years)
future_df = pd.DataFrame({
    '연도': future_years.flatten(),
    '예상 시간급': future_pred.astype(int)
})

# 📈 그래프 표시 (실제 + 예측)
st.markdown("### 최저임금의 미래 예측 그래프 📈")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', label='실제 최저임금')
ax.plot(future_df['연도'], future_df['예상 시간급'], marker='x', linestyle='--', color='orange', label='예상 최저임금')

if font_prop:
    ax.set_title("미래 최저임금 예측", fontproperties=font_prop)
    ax.set_xlabel("연도", fontproperties=font_prop)
    ax.set_ylabel("시간당 최저임금 (원)", fontproperties=font_prop)
    ax.legend(prop=font_prop)
else:
    ax.set_title("미래 최저임금 예측")
    ax.set_xlabel("연도")
    ax.set_ylabel("시간당 최저임금 (원)")
    ax.legend()

ax.grid(True)
st.pyplot(fig)

# 🔮 예측 결과 표
st.markdown("### 미래 최저임금 예측 결과 🔮")
st.dataframe(future_df)

# 📎 출처
st.markdown("---")
st.markdown("📌 데이터 출처: 고용노동부")
