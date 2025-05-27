import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")
st.title("📊 경기도 연령별 인구 시각화 (2025년 4월)")

# 수정된 경로 (pages 폴더 내에 있는 파일 기준)
total_path = "pages/202504_202504_연령별인구현황_계.csv"
mf_path = "pages/202504_202504_연령별인구현황_남녀.csv"

# 파일 존재 확인
if not os.path.exists(total_path) or not os.path.exists(mf_path):
    st.error("❌ CSV 파일이 존재하지 않습니다. 경로를 확인해 주세요.")
    st.stop()

# 데이터 로딩
df_total = pd.read_csv(total_path, encoding="cp949")
df_mf = pd.read_csv(mf_path, encoding="cp949")

# 연령 컬럼 추출
age_columns = [col for col in df_total.columns if "세" in col]
male_columns = [col for col in df_mf.columns if "남_" in col and "세" in col]
female_columns = [col for col in df_mf.columns if "여_" in col and "세" in col]

# 정확한 연령 라벨 추출
ages = [col.split('_')[-1] for col in age_columns]
ages = ["100+" if "이상" in age else age.replace("세", "") for age in ages]

# 인구 수 전처리
pop_total = df_total.loc[0, age_columns].fillna(0).astype(str).str.replace(",", "").astype(int)
pop_male = df_mf.loc[0, male_columns].fillna(0).astype(str).str.replace(",", "").astype(int)
pop_female = df_mf.loc[0, female_columns].fillna(0).astype(str).str.replace(",", "").astype(int)

# 데이터프레임 구성
df_plot = pd.DataFrame({
    "연령": ages,
    "연령 숫자": [int(age.replace("+", "")) for age in ages],
    "전체": pop_total,
    "남자": pop_male,
    "여자": pop_female
})

# 연령 필터
min_age, max_age = st.slider("🔍 보고 싶은 연령 범위를 선택하세요", 0, 100, (0, 100), step=5)
df_filtered = df_plot[(df_plot["연령 숫자"] >= min_age) & (df_plot["연령 숫자"] <= max_age)]

# 시각화 선택
chart_type = st.radio("📈 시각화 유형을 선택하세요", ["Bar", "Line", "Population Pyramid"], horizontal=True)

# 시각화
if chart_type == "Bar":
    fig = px.bar(
        df_filtered,
        x="연령",
        y="전체",
        title="전체 인구 (Bar)",
        color="전체",
        color_continuous_scale="Blues",
        hover_name="연령"
    )
    fig.update_traces(hovertemplate='연령: %{x}<br>인구 수: %{y}', marker=dict(line=dict(width=0.5, color='black')))
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line":
    fig = px.line(
        df_filtered,
        x="연령",
        y="전체",
        title="전체 인구 (Line)",
        markers=True,
        hover_name="연령"
    )
    fig.update_traces(hovertemplate='연령: %{x}<br>인구 수: %{y}', line=dict(width=2))
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Population Pyramid":
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_filtered["연령"],
        x=-df_filtered["남자"],
        name="남자",
        orientation='h',
        hovertemplate='연령: %{y}<br>남자: %{x}',
        marker=dict(color='lightblue', line=dict(width=1, color='darkblue'))
    ))
    fig.add_trace(go.Bar(
        y=df_filtered["연령"],
        x=df_filtered["여자"],
        name="여자"
