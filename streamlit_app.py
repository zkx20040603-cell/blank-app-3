# athlete_real_dashboard_kr.py

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="세계 육상 선수 실적 비교", layout="wide", page_icon="🏅")
st.title("🏅 세계 우수 육상 선수 개인 최고 기록 비교 대시보드")
st.markdown("""
이 대시보드는 위키백과(Wikipedia)에 공개된 선수들의 **개인 최고 기록(Personal Best)** 테이블을 가져와  
달리기 종목별로 비교하고 시각화합니다.
""")

st.divider()

# — 1) 분석할 선수와 위키피디아 URL 목록 —
athlete_pages = {
    "Usain Bolt": "https://en.wikipedia.org/wiki/Usain_Bolt",
    "Jakob Ingebrigtsen": "https://en.wikipedia.org/wiki/Jakob_Ingebrigtsen",
    "Karsten Warholm": "https://en.wikipedia.org/wiki/Karsten_Warholm",
    "Sydney McLaughlin-Levrone": "https://en.wikipedia.org/wiki/Sydney_McLaughlin-Levrone",
    "Elaine Thompson-Herah": "https://en.wikipedia.org/wiki/Elaine_Thompson-Herah"
}

st.sidebar.title("설정")
selected = st.sidebar.multiselect("분석할 선수 선택", list(athlete_pages.keys()), default=list(athlete_pages.keys()))
st.sidebar.markdown("⚠️ 위키피디아에서 데이터를 가져오므로 인터넷 연결이 필요합니다.")

# — 2) 위키피디아에서 '개인 최고 기록(Personal Best)' 테이블 추출 함수 —
@st.cache_data(show_spinner=False)
def fetch_personal_bests(url):
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        resp.raise_for_status()
    except Exception:
        return pd.DataFrame()
    try:
        tables = pd.read_html(resp.text)
    except Exception:
        return pd.DataFrame()

    candidate = None
    for t in tables:
        cols = [str(c).lower() for c in t.columns.astype(str)]
        flat = " ".join(cols)
        if ("personal" in flat and "best" in flat) or ("career statistics" in flat):
            candidate = t
            break
    if candidate is None:
        for t in tables:
            cols = [str(c).lower() for c in t.columns.astype(str)]
            if any(x in cols for x in ["event","performance","time","mark","result"]):
                candidate = t
                break
    if candidate is None:
        return pd.DataFrame()

    df = candidate.copy()
    df.columns = [str(c).strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if "event" in lc or "discipline" in lc:
            col_map[c] = "event"
        if "performance" in lc or "time" in lc or "mark" in lc or "result" in lc:
            col_map[c] = "performance"
        if "date" in lc:
            col_map[c] = "date"
    df = df.rename(columns=col_map)

    if "event" in df.columns and "performance" in df.columns:
        out = df[["event","performance"]].copy()
        if "date" in df.columns:
            out["date"] = df["date"]
    else:
        cols = list(df.columns)
        if len(cols) >= 2:
            out = df[[cols[0], cols[1]]].copy()
            out.columns = ["event","performance"]
            if len(cols) >= 3:
                out["date"] = df[cols[2]]
        else:
            return pd.DataFrame()

    out["event"] = out["event"].astype(str).str.replace(r"\[.*?\]","",regex=True).str.strip()
    out["performance"] = out["performance"].astype(str).str
