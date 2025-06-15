import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 등록
font_path = os.path.join(os.getcwd(), "NanumHumanRegular.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['axes.unicode_minus'] = False
    st.success("✅ NanumHumanRegular.ttf 폰트 불러오기 성공")
else:
    font_prop = None
    st.warning("⚠️ NanumHumanRegular.ttf 파일을 찾을 수 없습니다")

# ✅ 제목 (겹침 방지용 HTML 사용)
st.markdown("""
    <h1 style='font-size: 2.8em; margin-bottom: 0.5em;'>📊 최저임금의 연도별 변화</h1>
""", unsafe_allow_html=True)

# ✅ 여백 강제 삽입
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

# 📊 데이터 불러오기
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

# 📈 그래프 시각화
st.subheader("📈 최저임금의 연도별 변화")

fig, ax = plt.subplots()
ax.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2)

# ✅ 폰트 조건부 적용
if font_prop:
    ax.set_title('최저임금의 연도별 변화', fontproperties=font_prop)
    ax.set_xlabel('연도', fontproperties=font_prop)
    ax.set_ylabel('시간당 최저임금 (원)', fontproperties=font_prop)
else:
    ax.set_title('최저임금의 연도별 변화')
    ax.set_xlabel('연도')
    ax.set_ylabel('시간당 최저임금 (원)')

ax.grid(True)
st.pyplot(fig)

# 📎 출처
st.markdown("---")
st.markdown("📌 출처: 고용노동부")
