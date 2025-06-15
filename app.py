import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ NanumHumanRegular.ttf 폰트 등록 및 설정
font_path = os.path.join(os.getcwd(), "NanumHumanRegular.ttf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False
    st.success(f"✅ 한글 폰트 적용됨: `{font_name}`")
else:
    st.warning("⚠️ NanumHumanRegular.ttf 파일을 찾을 수 없습니다. 한글이 깨질 수 있어요.")

# 📌 앱 제목
st.title("📊 최저임금의 연도별 변화")

# 📊 CSV 데이터 로드
csv_file = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_file, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding="utf-8")

# 📂 데이터 정리
df = df[['연도', '시간급']]
df = df.sort_values('연도')

# 🧾 데이터 출력
st.subheader("🗂 최저임금 원본 데이터")
st.dataframe(df)

# 📈 그래프 출력
st.subheader("📉 최저임금의 연도별 변화")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2)
ax.set_xlabel('연도')
ax.set_ylabel('시간당 최저임금 (원)')
ax.set_title('최저임금의 연도별 변화')
ax.grid(True)

st.pyplot(fig)

# 📎 출처 표시
st.markdown("---")
st.markdown("📌 출처: 고용노동부 (https://www.moel.go.kr)")
