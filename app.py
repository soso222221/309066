import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정: NanumGothic-Bold.ttf가 루트에 있어야 합니다
font_path = os.path.join(os.getcwd(), "NanumGothic-Bold.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    plt.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False
    st.write(f"✅ 현재 적용된 폰트: `{NanumGothic-Bold.ttf}`")
else:
    st.warning("⚠️ NanumGothic-Bold.ttf 파일을 찾을 수 없습니다. 한글이 깨질 수 있어요.")

# 🎯 앱 제목
st.title("📈 연도별 최저임금 변화 그래프")

# 📊 CSV 데이터 불러오기
csv_path = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_path, encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding='utf-8')

# 📂 데이터 정제
df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 🗂️ 데이터프레임 출력
st.subheader("🗂️ 원본 데이터")
st.dataframe(df)

# 📈 그래프 시각화
st.subheader("📉 최저임금 연도별 변화")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2)
ax.set_xlabel('연도')
ax.set_ylabel('시간당 최저임금 (원)')
ax.set_title('최저임금의 연도별 변화')
ax.grid(True)

# 📌 그래프 출력
st.pyplot(fig)

# 🔗 출처
st.markdown("---")
st.markdown("📌 데이터 출처: 고용노동부")
