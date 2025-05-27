import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")
st.title("📊 경기도 연령별 인구 시각화 (2025년 4월)")

# 파일 경로 직접 지정 (사용자가 업로드하지 않아도 되도록)
total_path = "202504_202504_\uac00\uacfc\uacfc_\uacc4.csv"
mf_path = "202504_202504_\uac00\uacfc\uacfc_\ub0a8\ub140.csv"

# 데이터 로딩
df_total = pd.read_csv(total_path, encoding="cp949")
df_mf = pd.read_csv(mf_path, encoding="cp949")

# 연령 컬럼만 추출
age_columns = [col for col in df_total.columns if "세" in col]
ages = [col.split('_')[-1].replace("세", "") for col in age_columns]
ages = ["100+" if "이상" in age else age for age in ages]

# 전체 인구
pop_total = df_total.loc[0, age_columns].fillna(0).astype(str).str.replace(",", "").astype(int)

# 남녀 데이터
male_columns = [col for col in df_mf.columns if "남_" in col and "세" in col]
female_columns = [col for col in df_mf.columns if "여_" in col and "세" in col]

pop_male = df_mf.loc[0, male_columns].fillna(0).astype(str).str.replace(",", "").astype(int)
pop_female = df_mf.loc[0, female_columns].fillna(0).astype(str).str.replace(",", "").astype(int)

# 나이 정수형 정리
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

# 전체 인구 분포
if chart_type == "Bar":
    fig = px.bar(df_filtered, x="연령", y="전체", title="전체 인구 (Bar)", color="전체")
    st.plotly_chart(fig, use_container_width=True)
elif chart_type == "Line":
    fig = px.line(df_filtered, x="연령", y="전체", title="전체 인구 (Line)", markers=True)
    st.plotly_chart(fig, use_container_width=True)
elif chart_type == "Population Pyramid":
    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_filtered["연령"], x=-df_filtered["남자"], name="남자", orientation='h'))
    fig.add_trace(go.Bar(y=df_filtered["연령"], x=df_filtered["여자"], name="여자", orientation='h'))

    fig.update_layout(
        title="성별 인구 피라미드",
        barmode='relative',
        xaxis=dict(title='인구 수', tickvals=[-100000, -50000, 0, 50000, 100000], ticktext=['10만', '5만', '0', '5만', '10만']),
        yaxis=dict(title='연령'),
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# 데이터 다운로드
st.download_button("⬇️ 필터링된 인구 데이터 다운로드", data=df_filtered.to_csv(index=False), file_name="filtered_population.csv", mime="text/csv")
