import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")
st.title("📊 경기도 연령별 인구 시각화 (2025년 4월)")

# 파일 경로 (pages 폴더 기준)
total_path = "pages/202504_202504_연령별인구현황_계.csv"
mf_path = "pages/202504_202504_연령별인구현황_남녀.csv"

# 파일 존재 확인
if not os.path.exists(total_path) or not os.path.exists(mf_path):
    st.error("❌ CSV 파일이 존재하지 않습니다. 경로를 확인해 주세요.")
    st.stop()

# CSV 파일 불러오기 (쉼표 천 단위 숫자 처리)
try:
    df_total = pd.read_csv(total_path, encoding="cp949", thousands=',')
    df_mf = pd.read_csv(mf_path, encoding="cp949", thousands=',')
except Exception as e:
    st.error(f"❌ CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 연령 관련 컬럼 추출
age_columns = [col for col in df_total.columns if "세" in col]
male_columns = [col for col in df_mf.columns if "남_" in col and "세" in col]
female_columns = [col for col in df_mf.columns if "여_" in col and "세" in col]

# 연령 라벨 생성
ages = [col.split('_')[-1].replace("세", "") for col in age_columns]
ages = ["100+" if "이상" in age else age for age in ages]

# 인구 수 추출 (iloc 사용하여 Series 보장)
try:
    pop_total = df_total[age_columns].iloc[0].astype(int).tolist()
    pop_male = df_mf[male_columns].iloc[0].astype(int).tolist()
    pop_female = df_mf[female_columns].iloc[0].astype(int).tolist()
except Exception as e:
    st.error(f"❌ 인구 데이터를 처리하는 중 오류가 발생했습니다: {e}")
    st.stop()

# 길이 확인
if not (len(ages) == len(pop_total) == len(pop_male) == len(pop_female)):
    st.error("❌ 연령과 인구 데이터의 길이가 일치하지 않습니다. 파일을 확인해 주세요.")
    st.stop()

# 시각화용 데이터프레임 생성
df_plot = pd.DataFrame({
    "연령": ages,
    "연령 숫자": [int(age.replace("+", "")) for age in ages],
    "전체": pop_total,
    "남자": pop_male,
    "여자": pop_female
})

# 연령 필터 설정
min_age, max_age = st.slider("🔍 보고 싶은 연령 범위를 선택하세요", 0, 100, (0, 100), step=5)
df_filtered = df_plot[(df_plot["연령 숫자"] >= min_age) & (df_plot["연령 숫자"] <= max_age)]

# 시각화 타입 선택
chart_type = st.radio("📈 시각화 유형을 선택하세요", ["Bar", "Line", "Population Pyramid"], horizontal=True)

# 시각화 실행
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
    fig.update_traces(marker_line_width=0.5, marker_line_color='black')
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
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Population Pyramid":
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_filtered["연령"],
        x=[-val for val in df_filtered["남자"]],
        name="남자",
        orientation='h',
        marker=dict(color='lightblue', line=dict(width=1, color='darkblue')),
        hovertemplate='연령: %{y}<br>남자: %{x}'
    ))
    fig.add_trace(go.Bar(
        y=df_filtered["연령"],
        x=df_filtered["여자"],
        name="여자",
        orientation='h',
        marker=dict(color='pink', line=dict(width=1, color='deeppink')),
        hovertemplate='연령: %{y}<br>여자: %{x}'
    ))
    fig.update_layout(
        title="성별 인구 피라미드",
        barmode='relative',
        xaxis=dict(title='인구 수', tickvals=[-100000, -50000, 0, 50000, 100000], ticktext=['10만', '5만', '0', '5만', '10만']),
        yaxis=dict(title='연령'),
        template='plotly_white',
        hovermode='closest'
    )
    st.plotly_chart(fig, use_container_width=True)

# 데이터 다운로드
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="⬇️ 필터링된 인구 데이터 다운로드",
    data=csv,
    file_name="filtered_population.csv",
    mime="text/csv"
) 
