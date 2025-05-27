import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import datetime

st.set_page_config(page_title="재무 설계 및 글로벌 주식/ETF 시각화", layout="wide")
st.title("🌍 글로벌 시가총액 TOP 10 기업 주가 변화 + 맞춤 ETF 설계")

# ------------------------
# 글로벌 시가총액 Top 10
# ------------------------
top10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Meta": "META",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

st.header("📈 글로벌 시가총액 TOP10 주가 변화 (최근 1년)")
start_date = datetime.date.today() - datetime.timedelta(days=365)
end_date = datetime.date.today()

price_data = yf.download(list(top10_tickers.values()), start=start_date, end=end_date)['Adj Close']

# 주가 변동률 계산
growth_data = price_data.pct_change().add(1).cumprod().fillna(1)
growth_data.columns = list(top10_tickers.keys())

fig = px.line(growth_data, title="📊 최근 1년간 주가 수익률 추이 (%)")
fig.update_layout(yaxis_tickformat='.0%', template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ------------------------
# 설문조사: 투자 성향 파악
# ------------------------
st.header("🧠 투자 성향 설문조사")
risk = st.radio("당신의 투자 성향은?", ["안정형", "중립형", "공격형"], horizontal=True)
time_horizon = st.selectbox("투자 기간은 얼마인가요?", ["1년 이하", "1~3년", "3년 이상"])
goal = st.multiselect("주요 투자 목적을 선택하세요", ["자산 증식", "은퇴 대비", "단기 수익", "인플레이션 헤지"])

# ------------------------
# ETF 추천
# ------------------------
st.subheader("🔍 추천 ETF")
etf_suggestions = {
    "안정형": ["BND - 미국 총채권시장", "GLD - 금 ETF", "VNQ - 리츠"],
    "중립형": ["VOO - S&P500", "VTI - 미국 전체시장", "VT - 글로벌 종합"],
    "공격형": ["QQQ - 나스닥 성장주", "ARKK - 혁신 ETF", "SOXX - 반도체"]
}

for etf in etf_suggestions.get(risk, []):
    st.write(f"✅ {etf}")

# ------------------------
# 금 vs ETF 비교 시각화
# ------------------------
st.header("📊 금 vs ETF 비교")
comparison_etfs = ["GLD", "QQQ"]  # 금과 기술주 ETF
comparison_data = yf.download(comparison_etfs, start=start_date, end=end_date)['Adj Close']
comparison_growth = comparison_data.pct_change().add(1).cumprod().fillna(1)
fig2 = px.line(comparison_growth, title="금(GLD) vs 기술주(QQQ) 수익률 비교", labels={"value": "수익률", "Date": "날짜"})
fig2.update_layout(yaxis_tickformat='.0%', template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

st.success("🎯 설문 결과에 따라 추천된 ETF 목록을 확인하고, 수익률 비교 차트도 함께 분석해보세요!")
