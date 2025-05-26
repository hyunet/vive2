import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")
st.title("📊 경기도 연령별 전체 인구 (2025년 4월) 시각화")

uploaded_file = st.file_uploader("📁 CSV 파일을 업로드하세요 (예: 연령별인구현황_계.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 연령별 컬럼만 추출
    age_columns = [col for col in df.columns if "세" in col]
    population = df.loc[0, age_columns]

    # 연령 텍스트 정리
    ages = [col.split('_')[-1].replace("세", "") for col in age_columns]
    ages = ["100+" if "이상" in age else age for age in ages]

    # 숫자 처리
    population = population.fillna(0).astype(str).str.replace(",", "").astype(int)

    # 시각화용 데이터프레임
    df_plot = pd.DataFrame({"연령": ages, "인구 수": population})
    df_plot["연령 숫자"] = df_plot["연령"].str.replace("+", "").astype(int)

    # 슬라이더로 연령 필터링
    min_age, max_age = st.slider("🔍 보고 싶은 연령 범위를 선택하세요", 0, 100, (0, 100), step=5)
    filtered_df = df_plot[(df_plot["연령 숫자"] >= min_age) & (df_plot["연령 숫자"] <= max_age)]

    # 시각화 유형 선택
    chart_type = st.radio("📈 시각화 유형을 선택하세요", ["Bar", "Line", "Area", "Pie"], horizontal=True)

    st.subheader("📌 연령별 인구 시각화")

    # 차트 생성
    if chart_type == "Bar":
        fig = px.bar(filtered_df, x="연령", y="인구 수", title="연령별 인구 (Bar)", color="인구 수")
    elif chart_type == "Line":
        fig = px.line(filtered_df, x="연령", y="인구 수", title="연령별 인구 (Line)", markers=True)
    elif chart_type == "Area":
        fig = px.area(filtered_df, x="연령", y="인구 수", title="연령별 인구 (Area)")
    elif chart_type == "Pie":
        fig = px.pie(filtered_df, values="인구 수", names="연령", title="연령 구성 비율 (Pie)")

    st.plotly_chart(fig, use_container_width=True)

    # 인사이트 제공용 테이블
    st.subheader("📋 인구 상위/하위 연령대")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔝 상위 5개 연령대")
        st.dataframe(filtered_df.sort_values("인구 수", ascending=False).head(5), use_container_width=True)

    with col2:
        st.markdown("#### 🔻 하위 5개 연령대")
        st.dataframe(filtered_df.sort_values("인구 수").head(5), use_container_width=True)

    # 다운로드 기능
    st.download_button("⬇️ 현재 데이터 CSV 다운로드", data=filtered_df.to_csv(index=False), file_name="filtered_population.csv", mime="text/csv")
