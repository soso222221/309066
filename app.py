import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 나눔고딕 폰트 설정
font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")  # 정확히 NanumGothic.ttf 파일명
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    plt.rcParams['font.family'] = [font_name]  # 중요: 리스트로 설정
    plt.rcParams['axes.unicode_minus'] = False
    st.write(f"✅ 적용된 한글 폰트: `{font_name}`")
else:
    st.warning("⚠️ NanumGothic.ttf 파일을 찾을 수 없습니다. 한글이 깨질 수 있어요.")

# 📌 타이틀
st.title("📈 연도별 최저임금 변화 그래프")

# 📊 데이터 로드
csv_file = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_file, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding="utf-8")

# 📂 데이터 정제
df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 🧾 데이터 출력
st.subheader("🗂 최저임금 원본 데이터")
st.dataframe(df)

# 📉 시각화
st.subheader("📉 최저임금의 연도별 변화")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2)
ax.set_xlabel('연도')
ax.set_ylabel('시간당 최저임금 (원)')
ax.set_title('최저임금의 연도별 변화')
ax.grid(True)

# 출력
st.pyplot(fig)

# 출처
st.markdown("---")
st.markdown("📌 출처: 고용노동부 (https://www.moel.go.kr)")
