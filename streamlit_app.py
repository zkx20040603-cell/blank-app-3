import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 기본 설정 ---
st.set_page_config(
    page_title="육상 선수 성과 분석",
    page_icon="🏃‍♂️",
    layout="wide"
)

st.title("🏃‍♂️ 육상 선수 성과 분석 대시보드")
st.markdown("""
이 대시보드는 **육상 선수들의 기록, 성장 추세, 종목별 비교**를 시각적으로 분석하기 위해 제작되었습니다.
가상의 데이터를 기반으로 구성되었습니다.
""")

st.divider()

# --- 2. 가상 데이터 생성 ---
np.random.seed(42)
athletes = ["김민수", "박지훈", "최유진", "이서준", "정하늘"]
events = ["100m", "200m", "400m", "800m", "1500m"]

data_list = []
for athlete in athletes:
    for event in events:
        for year in [2021, 2022, 2023, 2024]:
            record = np.random.uniform(10.5, 15.5) if event == "100m" else \
                     np.random.uniform(21.0, 30.0) if event == "200m" else \
                     np.random.uniform(47.0, 60.0) if event == "400m" else \
                     np.random.uniform(110, 140) if event == "800m" else \
                     np.random.uniform(230, 300)
            data_list.append([athlete, event, year, round(record, 2)])

df = pd.DataFrame(data_list, columns=["선수", "종목", "연도", "기록"])

# --- 3. 사이드바 필터 ---
with st.sidebar:
    st.title("⚙️ 필터 설정")

    selected_athlete = st.selectbox("선수 선택", athletes)
    selected_event = st.multiselect("종목 선택", events, default=events)
    selected_year = st.multiselect("연도 선택", sorted(df["연도"].unique()), default=df["연도"].unique())

    show_raw = st.checkbox("📄 원본 데이터 보기")

# --- 4. 데이터 필터링 ---
filtered = df[
    (df["선수"] == selected_athlete) &
    (df["종목"].isin(selected_event)) &
    (df["연도"].isin(selected_year))
]

st.subheader(f"📊 {selected_athlete} 선수의 성과 요약")

# --- 5. KPI 카드 ---
best_record = filtered["기록"].min()
recent_record = filtered[filtered["연도"] == filtered["연도"].max()]["기록"].mean()

col1, col2 = st.columns(2)
col1.metric("🏅 최고 기록", f"{best_record}")
col2.metric("📉 최근 평균 기록", f"{round(recent_record, 2)}")

st.divider()

# --- 6. 시각화: 연도별 기록 추세 ---
st.subheader("📈 연도별 기록 변화")

fig_line = px.line(
    filtered,
    x="연도",
    y="기록",
    color="종목",
    markers=True
)
fig_line.update_layout(height=450)
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# --- 7. 시각화: 선수 종목별 능력 레이더 차트 ---
st.subheader("🕸 종목별 능력 레이더 차트")

radar_data = df[df["선수"] == selected_athlete].groupby("종목")["기록"].mean().reset_index()

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r = radar_data["기록"],
    theta = radar_data["종목"],
    fill='toself',
    name=selected_athlete
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False,
    height=500
)

st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# --- 8. 전체 선수 종목 비교 ---
st.subheader("🏆 선수별 종목 평균 기록 비교")

compare_df = df.groupby(["선수", "종목"])["기록"].mean().reset_index()

fig_bar = px.bar(
    compare_df,
    x="종목",
    y="기록",
    color="선수",
    barmode="group"
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- 9. 원본 데이터 ---
if show_raw:
    st.subheader("📄 원본 데이터")
    st.dataframe(filtered, use_container_width=True)

