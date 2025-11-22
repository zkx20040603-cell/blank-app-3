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
    selected_year = st.multiselect("연도 선택",_
