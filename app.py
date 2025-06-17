import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from prophet import Prophet
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

# ✅ Prophet 입력형식 변환
df_prophet = df.rename(columns={'연도': 'ds', '시간급': 'y'})
df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], format='%Y')

# ✅ Prophet 모델 생성 및 학습
model = Prophet(yearly_seasonality=False, daily_seasonality=False, weekly_seasonality=False)
model.fit(df_prophet)

# ✅ 미래 예측 (2026~2035)
last_year = df_prophet['ds'].dt.year.max()
future = model.make_future_dataframe(periods=2035-last_year, freq='Y')
forecast = model.predict(future)

# 예측 결과에서 2026~2035만 추출
forecast_future = forecast[forecast['ds'].dt.year > last_year][['ds', 'yhat']]
forecast_future['연도'] = forecast_future['ds'].dt.year
forecast_future['예상 시간급'] = forecast_future['yhat'].astype(int)
future_df = forecast_future[['연도', '예상 시간급']].reset_index(drop=True)

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
    # 예측(Prophet)
    ax2.plot(
        future_df['연도'], future_df['예상 시간급'],
        marker='D', linestyle=':', linewidth=3, color='purple', label='예상 최저임금(Prophet)'
    )
    if font_prop:
        ax2.set_title("미래 최저임금 예측 (Prophet)", fontproperties=font_prop)
        ax2.set_xlabel("연도", fontproperties=font_prop)
        ax2.set_ylabel("시간당 최저임금 (원)", fontproperties=font_prop)
        ax2.legend(prop=font_prop)
    else:
        ax2.set_title("미래 최저임금 예측 (Prophet)")
        ax2.set_xlabel("연도")
        ax2.set_ylabel("시간당 최저임금 (원)")
        ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

# 📎 출처
st.markdown("---")
st.markdown("📌 데이터 출처: 고용노동부")
