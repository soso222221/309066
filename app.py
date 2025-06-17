import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# ✅ 한글 폰트 설정
font_path = os.path.join(os.getcwd(), "NanumHumanRegular.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())
    plt.rcParams['axes.unicode_minus'] = False
    st.success("✅ NanumHumanRegular.ttf 폰트 적용 완료")
else:
    font_prop = None
    st.warning("⚠️ NanumHumanRegular.ttf 파일이 없습니다.")

# 📊 데이터 불러오기
csv_file = "고용노동부_연도별 최저임금_20240805.csv"
try:
    df = pd.read_csv(csv_file, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding="utf-8")

df = df[['연도', '시간급']]
df = df.sort_values('연도')

# ✅ 미래 예측: "잠깐 하락 후 쭉 상승" 패턴 직접 생성
last_real_year = df['연도'].max()
last_real_wage = df.loc[df['연도'] == last_real_year, '시간급'].values[0]

future_years = np.arange(last_real_year + 1, 2036)
future_wage = []

for idx, year in enumerate(future_years):
    if idx < 2:  # 예측 첫 2년(잠깐 하락)
        # 1년째: -2%, 2년째: -1% (약간 하락)
        pct = 0.98 if idx == 0 else 0.99
        wage = last_real_wage * pct
    elif idx < 4:  # 3~4년째(횡보 또는 소폭 반등)
        wage = last_real_wage * 1.00 + (idx - 1) * 150  # 약간 상승
    else:
        # 그 이후엔 매년 4~6% 상승(현실적 예측)
        wage = future_wage[-1] * np.random.uniform(1.04, 1.06)
    future_wage.append(int(wage))

future_df = pd.DataFrame({
    '연도': future_years,
    '예상 시간급': future_wage
})

# ✅ Streamlit 탭
tab1, tab2 = st.tabs(["📊 실제 데이터", "🤖 미래 예측"])

with tab1:
    st.markdown("### 최저임금 원본 데이터")
    st.dataframe(df)

    st.markdown("### 최저임금의 연도별 변화")
    fig, ax = plt.subplots()
    ax.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2, color='C0', label='실제 최저임금')
    if font_prop:
        ax.set_title("최저임금의 연도별 변화", fontproperties=font_prop)
        ax.set_xlabel("연도", fontproperties=font_prop)
        ax.set_ylabel("시간당 최저임금 (원)", fontproperties=font_prop)
        ax.legend(prop=font_prop)
    else:
        ax.set_title("최저임금의 연도별 변화")
        ax.set_xlabel("연도")
        ax.set_ylabel("시간당 최저임금 (원)")
        ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.markdown("### 미래 최저임금 예측 결과")
    st.dataframe(future_df)

    st.markdown("### 최저임금의 미래 예측 그래프")
    fig2, ax2 = plt.subplots()
    # 실제
    ax2.plot(df['연도'], df['시간급'], marker='o', linestyle='-', linewidth=2, color='C0', label='실제 최저임금')
    # 예측(잠깐 하락 후 쭉 상승)
    ax2.plot(
        future_df['연도'], future_df['예상 시간급'],
        marker='D', linestyle=':', linewidth=3, color='purple', label='예상 최저임금'
    )
    if font_prop:
        ax2.set_title("미래 최저임금 예측", fontproperties=font_prop)
        ax2.set_xlabel("연도", fontproperties=font_prop)
        ax2.set_ylabel("시간당 최저임금 (원)", fontproperties=font_prop)
        ax2.legend(prop=font_prop)
    else:
        ax2.set_title("미래 최저임금 예측")
        ax2.set_xlabel("연도")
        ax2.set_ylabel("시간당 최저임금 (원)")
        ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

# 📎 출처
st.markdown("---")
st.markdown("📌 데이터 출처: 고용노동부")
