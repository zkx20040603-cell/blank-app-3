import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="축구 선수 득점 분석",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ 축구 선수 득점 분석 대시보드")
st.markdown("""
이 대시보드는 축구 선수의 **득점 및 공격 지표**를 시각적으로 분석하기 위해 제작되었습니다.  
선수별, 시즌별, 리그별 데이터를 비교할 수 있습니다.
""")

st.divider()

# --- 2. 가상 데이터 생성 ---
np.random.seed(42)
players = ["손흥민", "케빈 데 브라위너", "리오넬 메시", "크리스티아누 호날두", "네이마르"]
seasons = ["2021/22", "2022/23", "2023/24"]
leagues = ["프리미어리그", "라리가", "세리에 A"]

data_list = []
for player in players:
    for season in seasons:
        for league in leagues:
            matches = np.random.randint(20, 40)
            goals = np.random.randint(0, matches)
            assists = np.random.randint(0, matches-goals+1)
            data_list.append([player, season, league, matches, goals, assists])

df = pd.DataFrame(data_list, columns=["선수", "시즌", "리그", "경기수", "득점", "도움"])

# --- 3. 사이드바 필터 ---
with st.sidebar:
    st.title("⚙️ 필터 설정")
    selected_player = st.multiselect("선수 선택", players, default=players)
    selected_season = st.multiselect("시즌 선택", seasons, default=seasons)
    selected_league = st.multiselect("리그 선택", leagues, default=leagues)
    show_raw = st.checkbox("📄 원본 데이터 보기", value=False)

# --- 4. 데이터 필터링 ---
filtered = df[
    (df["선수"].isin(selected_player)) &
    (df["시즌"].isin(selected_season)) &
    (df["리그"].isin(selected_league))
]

# --- 5. KPI 카드 ---
total_goals = int(filtered["득점"].sum())
total_assists = int(filtered["도움"].sum())
total_matches = int(filtered["경기수"].sum())
avg_goals_per_match = round(total_goals / total_matches, 2) if total_matches > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏆 총 득점", total_goals)
col2.metric("🎯 총 도움", total_assists)
col3.metric("⚽ 총 경기수", total_matches)
col4.metric("⚡ 경기당 평균 득점", avg_goals_per_match)

st.divider()

# --- 6. 시각화: 선수별 시즌별 득점 ---
st.subheader("📊 선수별 시즌별 득점 비교")
fig1 = px.bar(
    filtered,
    x="선수",
    y="득점",
    color="시즌",
    barmode="group",
    text="득점",
    labels={"득점":"득점", "선수":"선수"}
)
st.plotly_chart(fig1, use_container_width=True)

# --- 7. 시각화: 선수별 경기당 득점 추세 ---
st.subheader("📈 선수별 경기당 득점")
filtered["경기당 득점"] = filtered["득점"] / filtered["경기수"]
fig2 = px.line(
    filtered,
    x="시즌",
    y="경기당 득점",
    color="선수",
    markers=True,
    labels={"경기당 득점":"경기당 득점", "시즌":"시즌"}
)
st.plotly_chart(fig2, use_container_width=True)

# --- 8. 시각화: 레이더 차트 (득점 vs 도움) ---
st.subheader("🕸 선수별 공격력 비교 (득점 vs 도움)")
player_for_radar = st.selectbox("레이더 차트로 볼 선수 선택", selected_player)
radar_df = filtered[filtered["선수"] == player_for_radar]
if not radar_df.empty:
    goals_total = radar_df["득점"].sum()
    assists_total = radar_df["도움"].sum()
    categories = ["득점", "도움"]
    values = [goals_total, assists_total]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player_for_radar
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)),
                            showlegend=False, height=450)
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 9. 원본 데이터 표시 ---
if show_raw:
    st.divider()
    st.subheader("📄 필터링된 원본 데이터")
    st.dataframe(filtered, use_container_width=True)

