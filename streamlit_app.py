import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="날씨 데이터 대시보드",
    page_icon="🌤️",
    layout="wide"
)

# --- 2. 제목 및 설명 ---
st.title("🌤️ 날씨 데이터 대시보드")
st.markdown("""
이 대시보드는 **기온, 습도, 강수량** 등 기상 데이터를 시각적으로 분석하기 위해 만들어졌습니다.  
월별, 지역별 날씨 변화를 한눈에 확인할 수 있습니다.
""")

st.divider()

# --- 3. 가상 날씨 데이터 생성 ---
np.random.seed(42)
n = 3000

regions = ["서울", "부산", "대구", "광주", "대전", "인천"]

data = pd.DataFrame({
    "연도": np.random.choice([2022, 2023, 2024], n),
    "월": np.random.randint(1, 13, n),
    "지역": np.random.choice(regions, n),
    "기온(℃)": np.round(np.random.normal(15, 10, n), 1),
    "습도(%)": np.random.randint(30, 90, n),
    "강수량(mm)": np.round(np.random.gamma(2, 5, n), 1)
})

# --- 4. 사이드바 필터 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3314/3314000.png", width=100)
    st.title("⚙️ 필터 설정")

    year = st.multiselect("연도 선택", sorted(data["연도"].unique()), default=[2023])
    region = st.multiselect("지역 선택", regions, default=["서울", "부산"])
    metric_list = st.multiselect("지표 선택", ["기온(℃)", "습도(%)", "강수량(mm)"], default=["기온(℃)"])

    show_raw = st.checkbox("📄 원본 데이터 보기", value=False)

st.divider()

# --- 5. 데이터 필터링 ---
filtered = data[
    data["연도"].isin(year) &
    data["지역"].isin(region)
]

# --- 6. KPI 카드 ---
avg_temp = round(filtered["기온(℃)"].mean(), 1)
avg_humidity = int(filtered["습도(%)"].mean())
total_rain = round(filtered["강수량(mm)"].sum(), 1)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ 평균 기온", f"{avg_temp} ℃")
col2.metric("💧 평균 습도", f"{avg_humidity} %")
col3.metric("🌧️ 총 강수량", f"{total_rain} mm")

st.divider()

# --- 7. 시각화 영역 ---

# (1) 월별 기상 지표 라인 그래프
st.subheader("📅 월별 날씨 변화")

for metric in metric_list:
    fig = px.line(
        filtered.groupby(["연도", "월"])[metric].mean().reset_index(),
        x="월", y=metric, color="연도",
        markers=True
    )
    fig.update_layout(title=f"월별 평균 {metric}", height=350)
    st.plotly_chart(fig, use_container_width=True)

# (2) 지역별 평균 기온/습도/강수량
st.subheader("📍 지역별 날씨 비교")
metric_selected = st.selectbox("비교할 지표 선택", ["기온(℃)", "습도(%)", "강수량(mm)"])

fig2 = px.bar(
    filtered.groupby("지역")[metric_selected].mean().reset_index(),
    x="지역", y=metric_selected,
    text_auto=".2s",
    color="지역"
)
fig2.update_layout(showlegend=False, height=400)
st.plotly_chart(fig2, use_container_width=True)

# (3) 기온 분포 Box Plot
st.subheader("🌡️ 지역별 기온 분포")
fig3 = px.box(filtered, x="지역", y="기온(℃)", points="all")
st.plotly_chart(fig3, use_container_width=True)

# --- 8. 원본 데이터 보기 ---
if show_raw:
    st.divider()
    st.subheader("📄 필터링된 원본 데이터")
    st.dataframe(filtered, use_container_width=True)
